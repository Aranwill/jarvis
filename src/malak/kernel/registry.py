from typing import Dict, List, Optional

from malak.contracts.capability import Capability


class CapabilityRegistry:

    def __init__(self) -> None:
        self._capabilities: Dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:

        name = capability.name.lower()

        if name in self._capabilities:
            raise ValueError(f"Capability '{name}' is already registered.")

        self._capabilities[name] = capability

    def get(self, name: str) -> Optional[Capability]:

        return self._capabilities.get(name.lower())

    def list(self) -> List[str]:

        return sorted(self._capabilities.keys())