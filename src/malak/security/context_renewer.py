from datetime import timedelta

from malak.security.context_issuer import SecurityContextIssuer
from malak.security.context_validator import SecurityContextValidator
from malak.security.contracts import SecurityContext


class SecurityContextRenewer:
    def __init__(
        self,
        *,
        validator: SecurityContextValidator,
        issuer: SecurityContextIssuer,
    ) -> None:
        self._validator = validator
        self._issuer = issuer

    def renew(
        self,
        context: SecurityContext,
        *,
        lifetime: timedelta,
    ) -> SecurityContext:
        if not self._validator.is_valid(context):
            raise ValueError("cannot renew an expired security context")

        return self._issuer.issue(
            session_id=context.session_id,
            subject_id=context.subject_id,
            authenticated=context.authenticated,
            lifetime=lifetime,
            parent_context_id=context.context_id,
        )