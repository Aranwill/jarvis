from malak.contracts.capability import Capability


class EchoCapability(Capability):

    @property
    def name(self) -> str:
        return "echo"

    def execute(self, request):
        return request