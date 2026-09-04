from malak.contracts.capability import Capability
from malak.core.request import Request


class EchoCapability(Capability):

    @property
    def name(self) -> str:
        return "echo"

    def execute(self, request: Request):
        return request.content