from __future__ import annotations

from abc import ABC, abstractmethod

from malak.core.request import Request


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
    def execute(self, request: Request):
        """
        Execute the capability.
        """
        raise NotImplementedError