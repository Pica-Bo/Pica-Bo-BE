from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any, Dict, List, Optional, Sequence

import jwt
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.util.error_handling import UnauthorizedError, ForbiddenError

logger = logging.getLogger(__name__)


@dataclass
class AuthContext:
    """Authentication context extracted from a validated Zitadel JWT.

    This is returned by the auth dependency and can be injected into routes.
    """

    user_id: str
    client_id: str
    issuer: str
    claims: Dict[str, Any]
    name: str
    email: str


class _JWKSClientCache:
    """Simple cache of PyJWKClient instances per JWKS URL.

    PyJWT's PyJWKClient already caches keys in memory; this class just
    ensures we reuse the client per URL so JWKS is fetched periodically
    instead of on every request.
    """

    def __init__(self) -> None:
        self._clients: Dict[str, jwt.PyJWKClient] = {}

    def get_client(self, jwks_url: str) -> jwt.PyJWKClient:
        if jwks_url not in self._clients:
            self._clients[jwks_url] = jwt.PyJWKClient(jwks_url)
        return self._clients[jwks_url]


_jwks_cache = _JWKSClientCache()


# Bearer auth scheme for OpenAPI/Swagger UI.
_bearer_scheme = HTTPBearer(auto_error=False)


def _extract_bearer_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    if credentials is None or not credentials.scheme or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError("Missing or invalid Authorization header")

    if not credentials.credentials:
        raise UnauthorizedError("Missing bearer token")

    return credentials.credentials


def _decode_with_provider(token: str, provider: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Try to decode and verify a JWT for a single provider.

    Returns the decoded claims if successful, otherwise None.
    """

    issuer = provider.get("issuer")
    jwks_url = provider.get("jwks_url")
    audience = provider.get("audience") or None

    if not issuer or not jwks_url:
        return None

    jwks_client = _jwks_cache.get_client(jwks_url)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except Exception as e:
        logger.debug(f"Failed to get signing key from JWKS: {e}")
        return None

    algorithms: List[str] = []
    if getattr(signing_key, "algorithm", None):
        algorithms = [signing_key.algorithm]

    if not algorithms:
        algorithms = ["RS256", "PS256", "ES256"]

    decode_kwargs: Dict[str, Any] = {
        "key": signing_key.key,
        "algorithms": algorithms,
        "issuer": issuer,
    }
    if audience:
        decode_kwargs["audience"] = audience

    try:
        return jwt.decode(token, **decode_kwargs)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("JWT has expired")
    except jwt.InvalidTokenError:
        return None


def _decode_and_verify_token(
    token: str,
    provider_keys: Optional[Sequence[str]] = None,
    allowed_client_ids: Optional[Sequence[str]] = None,
) -> AuthContext:
    """Decode and verify a JWT against one or more configured providers.

    If ``provider_keys`` is given, only those providers are tried. Otherwise all
    providers in ``settings.zitadel_providers`` are considered.
    """

    providers_map = settings.zitadel_providers
    if provider_keys:
        providers = [providers_map[key] for key in provider_keys if key in providers_map]
    else:
        providers = list(providers_map.values())

    claims: Optional[Dict[str, Any]] = None
    matched_provider: Optional[Dict[str, Any]] = None

    # Try the selected providers until one successfully validates the token.
    for provider in providers:
        claims = _decode_with_provider(token, provider)
        if claims is not None:
            matched_provider = provider
            break

    if claims is None or matched_provider is None:
        raise UnauthorizedError("Failed to validate JWT for any configured provider")

    issuer = claims.get("iss")
    user_id = claims.get("sub")
    client_id = claims.get("client_id")
    name = claims.get("name")
    email = claims.get("email")

    if not issuer or not user_id or not client_id:
        raise UnauthorizedError("JWT is missing required claims (iss, sub, client_id)")

    configured_client_id = matched_provider.get("client_id")

    if configured_client_id and configured_client_id != client_id:
        raise UnauthorizedError("Token client_id does not match configured application")

    if allowed_client_ids is not None and client_id not in allowed_client_ids:
        raise ForbiddenError("Client is not allowed to access this resource")

    return AuthContext(user_id=user_id, client_id=client_id, issuer=issuer, claims=claims, name=name, email=email)


def require_zitadel_client(
    provider_keys: Optional[Sequence[str]] = None,
    allowed_client_ids: Optional[Sequence[str]] = None,
):
    """Factory for a FastAPI dependency that validates a Zitadel JWT.

    - Reads the bearer token from the Authorization header.
    - Verifies signature against the configured JWKS URL.
    - Enforces issuer and (optional) audience from settings.zitadel_providers.
    - Optionally restricts access to a set of allowed client_ids.

    Usage in a router::

        from fastapi import Depends
        from app.util.functions.auth import operator_auth

        @router.get("/", dependencies=[Depends(operator_auth)])
        async def list_resources(...):
            ...

    You can also inject the returned AuthContext if you need user_id/client_id
    inside the endpoint::

        @router.get("/")
        async def list_resources(current_auth: AuthContext = Depends(operator_auth)):
            ...
    """

    def _dependency(
        credentials: HTTPAuthorizationCredentials | None = Security(_bearer_scheme),
    ) -> AuthContext:
        token = _extract_bearer_token(credentials)
        return _decode_and_verify_token(
            token,
            provider_keys=provider_keys,
            allowed_client_ids=allowed_client_ids,
        )

    return _dependency


# Preconfigured dependencies by logical application type, based on env client_ids.
operator_auth = require_zitadel_client(
    provider_keys=["operator_app"],
    allowed_client_ids=[settings.zitadel_operator_client_id] if settings.zitadel_operator_client_id else None,
)

explorer_auth = require_zitadel_client(
    provider_keys=["explorer_app"],
    allowed_client_ids=[settings.zitadel_explorer_client_id] if settings.zitadel_explorer_client_id else None,
)

internal_service_auth = require_zitadel_client(
    provider_keys=["internal_service"],
    allowed_client_ids=[settings.internal_service_client_id] if settings.internal_service_client_id else None,
)
