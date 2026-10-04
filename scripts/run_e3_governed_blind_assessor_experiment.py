from __future__ import annotations

"""RED candidate for E3 Governed Blind Assessor Experiment Harness V0.

The public seams are intentionally present while behavior remains unimplemented.
GREEN is not authorized by this commit.
"""

from pathlib import Path
from typing import Any, Callable


PROFILE_SCHEMA = "MALAK-E3-BLIND-ASSESSOR-EXPERIMENT-PROFILE/v0"
HARNESS_POLICY_VERSION = "e3-governed-blind-assessor-experiment-harness/v0"
RESULTS_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1"
CASE_SET_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0.1"

NETWORK_AUTHORIZED = False
REPO_WRITES_AUTHORIZED = False
SUPPORT_SUFFICIENT_WIRING_AUTHORIZED = False
MODEL_PROVIDER_EXECUTION_AUTHORIZED = False
RDD_STAGE_2_AUTHORIZED = False
AUTHORITY_EFFECT = "none"


class ExperimentProfileError(ValueError):
    """Fail-closed profile validation error."""


class ExperimentBindingError(ValueError):
    """Fail-closed expected-profile/mechanism/harness binding error."""


def load_experiment_profile_v0(path: Path) -> dict[str, Any]:
    """Load and strictly validate the frozen V0 experiment profile."""
    raise NotImplementedError("RED: strict experiment profile loader is not implemented")


def build_expected_harness_v0(profile: dict[str, Any]) -> dict[str, str]:
    """Derive the exact four-field expected harness object from a validated profile."""
    raise NotImplementedError("RED: expected harness derivation is not implemented")


def verify_expected_experiment_binding_v0(
    *,
    profile: dict[str, Any],
    artifact: dict[str, Any],
) -> None:
    """Fail closed unless mechanism and full expected_harness match exactly."""
    raise NotImplementedError("RED: expected experiment binding verifier is not implemented")


def run_governed_blind_assessor_experiment_v0(
    *,
    case_set_path: Path,
    profile_path: Path,
    assessor: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """Produce RESULTS/v0.1 from the exact case-set through the governed blind path."""
    raise NotImplementedError("RED: governed blind assessor experiment harness is not implemented")
