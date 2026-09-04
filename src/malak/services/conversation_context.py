"""Contexto conversacional efímero y limitado de Malāk."""

from malak.core.conversation import ConversationMessage


class InMemoryConversationContext:
    """Conserva intercambios conversacionales aislados por sesión en memoria."""

    def __init__(self, max_exchanges: int = 6) -> None:
        if max_exchanges <= 0:
            raise ValueError("max_exchanges must be greater than zero")

        self._max_exchanges = max_exchanges
        self._sessions: dict[
            str,
            list[tuple[ConversationMessage, ConversationMessage]],
        ] = {}

    def snapshot(
        self,
        session_id: str,
    ) -> tuple[ConversationMessage, ...]:
        """Devuelve una vista inmutable del historial de una sesión."""
        exchanges = self._sessions.get(session_id, ())

        return tuple(
            message
            for exchange in exchanges
            for message in exchange
        )

    def record_exchange(
        self,
        session_id: str,
        user_content: str,
        assistant_content: str,
    ) -> None:
        """Registra un intercambio completo dentro de una sesión."""
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

        exchanges = self._sessions.setdefault(
            session_id,
            [],
        )
        exchanges.append(exchange)

        if len(exchanges) > self._max_exchanges:
            del exchanges[0]

    def clear(self, session_id: str) -> None:
        """Elimina únicamente los intercambios de una sesión."""
        self._sessions.pop(session_id, None)
