from __future__ import annotations

from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any, Dict


@dataclass
class DomainError(Exception):
    """Base domain-level error, independent of HTTP/FastAPI."""

    code: str
    message: str
    status_code: int
    details: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.code}: {self.message}"


class NotFoundError(DomainError):
    def __init__(self, resource: str = "Resource", details: Dict[str, Any] | None = None) -> None:
        super().__init__(
            code="not_found",
            message=f"{resource} not found",
            status_code=HTTPStatus.NOT_FOUND,
            details=details or {},
        )


class BadRequestError(DomainError):
    def __init__(self, message: str, details: Dict[str, Any] | None = None) -> None:
        super().__init__(
            code="bad_request",
            message=message,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details or {},
        )


class UnauthorizedError(DomainError):
    def __init__(self, message: str = "Unauthorized", details: Dict[str, Any] | None = None) -> None:
        super().__init__(
            code="unauthorized",
            message=message,
            status_code=HTTPStatus.UNAUTHORIZED,
            details=details or {},
        )


class ForbiddenError(DomainError):
    def __init__(self, message: str = "Forbidden", details: Dict[str, Any] | None = None) -> None:
        super().__init__(
            code="forbidden",
            message=message,
            status_code=HTTPStatus.FORBIDDEN,
            details=details or {},
        )


class ConflictError(DomainError):
    def __init__(self, message: str, details: Dict[str, Any] | None = None) -> None:
        super().__init__(
            code="conflict",
            message=message,
            status_code=HTTPStatus.CONFLICT,
            details=details or {},
        )


class ValidationDomainError(DomainError):
    def __init__(self, message: str, details: Dict[str, Any] | None = None) -> None:
        super().__init__(
            code="validation_error",
            message=message,
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            details=details or {},
        )
