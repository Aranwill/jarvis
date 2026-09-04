from malak.contracts.capability import Capability
from malak.core.conversation import ConversationRequest
from malak.core.request import Request
from malak.services.conversation_service import ConversationService


class ConversationCapability(Capability):
    """
    Adapts the generic capability execution boundary to ConversationService.
    """

    def __init__(
        self,
        service: ConversationService,
        provider_name: str,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> None:
        self._service = service
        self._provider_name = provider_name
        self._model = model
        self._system_prompt = system_prompt

    @property
    def name(self) -> str:
        return "conversation"

    def execute(self, request: Request):
        conversation_request = ConversationRequest(
            prompt=request.content,
            model=self._model,
            system_prompt=self._system_prompt,
        )

        response = self._service.generate(
            request=conversation_request,
            provider=self._provider_name,
            session_id=request.session_id,
        )

        return response.content
