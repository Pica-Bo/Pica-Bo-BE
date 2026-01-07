from typing import Dict

from pydantic import BaseSettings


class Settings(BaseSettings):
    # All values are loaded from environment variables or .env (no hard-coded defaults)
    mongo_uri: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_exp_minutes: int
    app_host: str
    app_port: int
    # Redis connection (for health checks and caching)
    redis_host: str
    redis_port: int
    # Optional admin bootstrap credentials (kept for backward compatibility, not used for auth)
    admin_email: str | None = None
    admin_password: str | None = None

    # ZITADEL / external issuers configuration
    # Individual env vars so deployments can override values per app.
    zitadel_operator_issuer: str
    zitadel_operator_audience: str
    zitadel_operator_jwks_url: str

    zitadel_explorer_issuer: str
    zitadel_explorer_audience: str
    zitadel_explorer_jwks_url: str

    internal_service_issuer: str
    internal_service_audience: str
    internal_service_jwks_url: str

    @property
    def zitadel_providers(self) -> Dict[str, dict]:
        """Structured view of configured JWT issuers for external auth.

        This is used for validating tokens from Zitadel and internal services.
        Do not embed secrets here; these are public issuer/audience/JWKS values.
        """

        return {
            "operator_app": {
                "issuer": self.zitadel_operator_issuer,
                "audience": self.zitadel_operator_audience,
                "jwks_url": self.zitadel_operator_jwks_url,
            },
            "explorer_app": {
                "issuer": self.zitadel_explorer_issuer,
                "audience": self.zitadel_explorer_audience,
                "jwks_url": self.zitadel_explorer_jwks_url,
            },
            "internal_service": {
                "issuer": self.internal_service_issuer,
                "audience": self.internal_service_audience,
                "jwks_url": self.internal_service_jwks_url,
            },
        }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
