from typing import Any, Optional

from app.util.error_handling import (
    BadRequestError,
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationDomainError,
)


class BaseService:
    """Common helpers for all services (domain error helpers)."""

    def _error(
        self,
        *,
        error: DomainError,
    ) -> None:
        """Raise a domain error; wrapper kept for symmetry/extensibility."""

        raise error

    def _not_found(self, resource: str = "Resource", details: Optional[dict[str, Any]] = None) -> None:
        self._error(error=NotFoundError(resource=resource, details=details or {}))

    def _bad_request(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        self._error(error=BadRequestError(message=message, details=details or {}))

    def _unauthorized(self, message: str = "Unauthorized", details: Optional[dict[str, Any]] = None) -> None:
        self._error(error=UnauthorizedError(message=message, details=details or {}))

    def _forbidden(self, message: str = "Forbidden", details: Optional[dict[str, Any]] = None) -> None:
        self._error(error=ForbiddenError(message=message, details=details or {}))

    def _conflict(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        self._error(error=ConflictError(message=message, details=details or {}))

    def _validation_error(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        self._error(error=ValidationDomainError(message=message, details=details or {}))
