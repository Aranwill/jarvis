"""Contexto conversacional efímero y limitado de Malāk."""

from malak.core.conversation import ConversationMessage


class InMemoryConversationContext:
    """Conserva intercambios conversacionales completos únicamente en memoria."""

    def __init__(self, max_exchanges: int = 6) -> None:
        if max_exchanges <= 0:
            raise ValueError("max_exchanges must be greater than zero")

        self._max_exchanges = max_exchanges
        self._exchanges: list[
            tuple[ConversationMessage, ConversationMessage]
        ] = []

    def snapshot(self) -> tuple[ConversationMessage, ...]:
        """Devuelve una vista inmutable del historial conversacional actual."""
        return tuple(
            message
            for exchange in self._exchanges
            for message in exchange
        )

    def record_exchange(
        self,
        user_content: str,
        assistant_content: str,
    ) -> None:
        """Registra un intercambio completo y aplica la ventana configurada."""
        exchange = (
            ConversationMessage(
                role="user",
                content=user_content,
            ),
            ConversationMessage(
                role="assistant",
                content=assistant_content,
            ),
        )

        self._exchanges.append(exchange)

        if len(self._exchanges) > self._max_exchanges:
            del self._exchanges[0]

    def clear(self) -> None:
        """Elimina todos los intercambios de la conversación activa."""
        self._exchanges.clear()