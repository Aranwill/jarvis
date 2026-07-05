from __future__ import annotations

from abc import ABC, abstractmethod


class Capability(ABC):
    """
    Base contract for every Malāk capability.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Public capability name.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, request):
        """
        Execute the capability.
        """
        raise NotImplementedError