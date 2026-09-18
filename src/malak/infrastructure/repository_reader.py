from __future__ import annotations

import hashlib
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

_MAX_TEXT_BYTES = 256 * 1024
_MAX_SEARCH_RESULTS = 100
_MAX_TRACKED_BLOBS = 4096
_MAX_SEARCHABLE_BYTES = 16 * 1024 * 1024
_MAX_SEARCH_BLOBS = 512
_MAX_SEARCH_OUTPUT_BYTES = 256 * 1024
_MAX_QUERY_BYTES = 4096
_GIT_TIMEOUT_SECONDS = 5.0
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:/")


@dataclass(frozen=True)
class RepositoryTextDocument:
    baseline_commit: str
    path: str
    blob_sha: str
    content: str


@dataclass(frozen=True)
class RepositoryTextMatch:
    baseline_commit: str
    path: str
    blob_sha: str
    line_number: int
    line: str


@dataclass(frozen=True)
class RepositorySearchResult:
    baseline_commit: str
    matches: tuple[RepositoryTextMatch, ...]
    truncated: bool


@dataclass(frozen=True)
class _TreeEntry:
    mode: str
    object_type: str
    object_sha: str
    size: int | None
    path: str

    @property
    def is_regular_file(self) -> bool:
        return self.object_type == "blob" and self.mode in {"100644", "100755"}


class GitRepositoryReader:
    """
    Read-only, commit-bound view over one exact Git repository snapshot.

    The reader captures HEAD and its tree during initialization. Subsequent reads
    address exact Git blob object IDs from that captured tree; working-tree,
    index, untracked and later-HEAD changes are therefore outside the view.
    """

    def __init__(
        self,
        repo_root: str | Path,
        *,
        max_text_bytes: int = _MAX_TEXT_BYTES,
        max_search_results: int = _MAX_SEARCH_RESULTS,
    ) -> None:
        self._max_text_bytes = _validated_limit(
            max_text_bytes,
            name="max_text_bytes",
            hard_max=_MAX_TEXT_BYTES,
        )
        self._max_search_results = _validated_limit(
            max_search_results,
            name="max_search_results",
            hard_max=_MAX_SEARCH_RESULTS,
        )

        root = Path(repo_root).expanduser()
        if not root.is_dir():
            raise RuntimeError("repository root is not an existing directory")

        self._repo_root = root.resolve()
        top_level = self._git_text("rev-parse", "--show-toplevel")
        try:
            resolved_top_level = Path(top_level).resolve()
        except (OSError, RuntimeError) as exc:
            raise RuntimeError("Git top-level path could not be resolved") from exc

        if resolved_top_level != self._repo_root:
            raise ValueError("repository root must be the exact Git top-level")

        baseline_commit = self._git_text("rev-parse", "HEAD")
        if not _SHA1_RE.fullmatch(baseline_commit):
            raise RuntimeError("Git HEAD is not a supported 40-character commit SHA")

        self._baseline_commit = baseline_commit
        self._entries = self._capture_tree(baseline_commit)

    @property
    def baseline_commit(self) -> str:
        return self._baseline_commit

    def list_tracked_files(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                entry.path
                for entry in self._entries.values()
                if entry.object_type == "blob"
            )
        )

    def read_text(self, path: str) -> RepositoryTextDocument:
        entry = self._entry_for_path(path)
        content = self._read_entry_text(entry)

        return RepositoryTextDocument(
            baseline_commit=self._baseline_commit,
            path=entry.path,
            blob_sha=entry.object_sha,
            content=content,
        )

    def search_text(self, query: str) -> RepositorySearchResult:
        _validate_query(query)

        eligible_entries = tuple(
            sorted(
                (
                    entry
                    for entry in self._entries.values()
                    if entry.is_regular_file
                    and entry.size is not None
                    and entry.size <= self._max_text_bytes
                ),
                key=lambda entry: entry.path,
            )
        )
        if len(eligible_entries) > _MAX_SEARCH_BLOBS:
            raise RuntimeError(
                "captured snapshot exceeds the hard E0 searchable-blob limit"
            )

        searchable_bytes = sum(entry.size for entry in eligible_entries)
        if searchable_bytes > _MAX_SEARCHABLE_BYTES:
            raise RuntimeError(
                "captured snapshot exceeds the hard E0 searchable-byte limit"
            )

        matches: list[RepositoryTextMatch] = []
        output_bytes = 0

        for entry in eligible_entries:
            try:
                content = self._read_entry_text(entry)
            except ValueError:
                continue

            for line_number, line in enumerate(content.splitlines(), start=1):
                if query not in line:
                    continue

                if len(matches) >= self._max_search_results:
                    return RepositorySearchResult(
                        baseline_commit=self._baseline_commit,
                        matches=tuple(matches),
                        truncated=True,
                    )

                line_bytes = len(line.encode("utf-8"))
                if output_bytes + line_bytes > _MAX_SEARCH_OUTPUT_BYTES:
                    return RepositorySearchResult(
                        baseline_commit=self._baseline_commit,
                        matches=tuple(matches),
                        truncated=True,
                    )

                matches.append(
                    RepositoryTextMatch(
                        baseline_commit=self._baseline_commit,
                        path=entry.path,
                        blob_sha=entry.object_sha,
                        line_number=line_number,
                        line=line,
                    )
                )
                output_bytes += line_bytes

        return RepositorySearchResult(
            baseline_commit=self._baseline_commit,
            matches=tuple(matches),
            truncated=False,
        )

    def _entry_for_path(self, path: str) -> _TreeEntry:
        logical_path = _validate_logical_path(path)
        entry = self._entries.get(logical_path)
        if entry is None:
            raise FileNotFoundError(f"path is not tracked in captured snapshot: {logical_path}")
        if not entry.is_regular_file:
            raise ValueError(f"path is not a regular text-file candidate: {logical_path}")
        return entry

    def _read_entry_text(self, entry: _TreeEntry) -> str:
        if entry.size is None:
            raise ValueError(f"tracked object has no readable blob size: {entry.path}")
        if entry.size > self._max_text_bytes:
            raise ValueError(
                f"tracked blob exceeds text limit of {self._max_text_bytes} bytes: {entry.path}"
            )

        raw = self._git_bytes("cat-file", "blob", entry.object_sha)
        if len(raw) != entry.size:
            raise RuntimeError(f"Git blob size mismatch for captured path: {entry.path}")

        git_object = f"blob {len(raw)}\0".encode("ascii") + raw
        actual_sha = hashlib.sha1(git_object, usedforsecurity=False).hexdigest()
        if actual_sha != entry.object_sha:
            raise RuntimeError(f"Git blob identity mismatch for captured path: {entry.path}")

        if b"\x00" in raw:
            raise ValueError(f"tracked blob is not textual content: {entry.path}")

        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"tracked blob is not valid UTF-8 text: {entry.path}") from exc

    def _capture_tree(self, commit: str) -> dict[str, _TreeEntry]:
        raw = self._git_bytes(
            "ls-tree",
            "-r",
            "-z",
            "-l",
            "--full-tree",
            commit,
        )

        entries: dict[str, _TreeEntry] = {}
        tracked_blobs = 0
        for record in raw.split(b"\x00"):
            if not record:
                continue

            try:
                metadata, raw_path = record.split(b"\t", 1)
                mode_raw, type_raw, sha_raw, size_raw = metadata.split()
            except ValueError as exc:
                raise RuntimeError("Git tree output has an unexpected format") from exc

            try:
                mode = mode_raw.decode("ascii")
                object_type = type_raw.decode("ascii")
                object_sha = sha_raw.decode("ascii")
                path = raw_path.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise RuntimeError("Git tree contains unsupported non-UTF-8 metadata or path") from exc

            try:
                _validate_logical_path(path)
            except (TypeError, ValueError) as exc:
                raise RuntimeError("Git tree contains a path unsupported by E0") from exc

            if not _SHA1_RE.fullmatch(object_sha):
                raise RuntimeError("Git tree contains an unsupported object identifier")

            size: int | None
            if size_raw == b"-":
                size = None
            else:
                try:
                    size = int(size_raw)
                except ValueError as exc:
                    raise RuntimeError("Git tree contains an invalid object size") from exc
                if size < 0:
                    raise RuntimeError("Git tree contains a negative object size")

            if path in entries:
                raise RuntimeError(f"Git tree contains a duplicate path: {path}")

            if object_type == "blob":
                tracked_blobs += 1
                if tracked_blobs > _MAX_TRACKED_BLOBS:
                    raise RuntimeError(
                        "captured snapshot exceeds the hard E0 tracked-blob limit"
                    )

            entries[path] = _TreeEntry(
                mode=mode,
                object_type=object_type,
                object_sha=object_sha,
                size=size,
                path=path,
            )

        return entries

    def _git_text(self, *args: str) -> str:
        raw = self._git_bytes(*args)
        try:
            return raw.decode("utf-8").strip()
        except UnicodeDecodeError as exc:
            raise RuntimeError("Git returned non-UTF-8 command output") from exc

    def _git_bytes(self, *args: str) -> bytes:
        command = [
            "git",
            "--no-replace-objects",
            "-C",
            str(self._repo_root),
            *args,
        ]
        try:
            completed = subprocess.run(
                command,
                check=False,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                timeout=_GIT_TIMEOUT_SECONDS,
                env=_git_environment(),
            )
        except FileNotFoundError as exc:
            raise RuntimeError("Git executable is unavailable") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("Git read-only inspection timed out") from exc
        except OSError as exc:
            raise RuntimeError("Git read-only inspection could not start") from exc

        if completed.returncode != 0:
            message = completed.stderr.decode("utf-8", errors="replace").strip()
            if len(message) > 512:
                message = f"{message[:512]}..."
            detail = f": {message}" if message else ""
            raise RuntimeError(
                f"Git read-only inspection failed with exit code {completed.returncode}{detail}"
            )

        return completed.stdout


def _validated_limit(value: int, *, name: str, hard_max: int) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    if value > hard_max:
        raise ValueError(f"{name} cannot exceed hard E0 limit {hard_max}")
    return value


def _validate_logical_path(path: str) -> str:
    if not isinstance(path, str):
        raise TypeError("repository path must be a string")
    if not path:
        raise ValueError("repository path cannot be empty")
    if any(ord(character) < 32 or ord(character) == 127 for character in path):
        raise ValueError("repository path contains forbidden control characters")
    if "\\" in path:
        raise ValueError("repository path must use POSIX separators")
    if path.startswith("/") or _WINDOWS_DRIVE_RE.match(path):
        raise ValueError("repository path must be relative")

    segments = path.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise ValueError("repository path must be canonical and traversal-free")

    canonical = PurePosixPath(path).as_posix()
    if canonical != path:
        raise ValueError("repository path must be canonical")

    return path


def _validate_query(query: str) -> None:
    if not isinstance(query, str):
        raise TypeError("search query must be a string")
    if not query:
        raise ValueError("search query cannot be empty")
    if any(ord(character) < 32 or ord(character) == 127 for character in query):
        raise ValueError("search query contains forbidden control characters")
    if len(query.encode("utf-8")) > _MAX_QUERY_BYTES:
        raise ValueError(
            f"search query cannot exceed {_MAX_QUERY_BYTES} UTF-8 bytes"
        )



def _git_environment() -> dict[str, str]:
    env = os.environ.copy()

    for key in tuple(env):
        if key.startswith("GIT_"):
            env.pop(key, None)

    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_PAGER"] = "cat"

    return env
