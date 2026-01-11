from typing import Dict

from pydantic import BaseSettings

from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # All values are loaded from environment variables or .env (no hard-coded defaults)
    mongo_uri: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/mydatabase")
    jwt_secret: str = os.getenv("JWT_SECRET", "change_me_to_a_strong_secret")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_exp_minutes: int = int(os.getenv("JWT_EXP_MINUTES", "60"))
    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    # Redis connection (for health checks and caching)
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    # Optional admin bootstrap credentials (kept for backward compatibility, not used for auth)
    admin_email: str | None = None
    admin_password: str | None = None

    # ZITADEL / external issuers configuration
    # Individual env vars so deployments can override values per app.
    zitadel_operator_issuer: str = os.getenv("ZITADEL_OPERATOR_ISSUER", "")
    zitadel_operator_audience: str = os.getenv("ZITADEL_OPERATOR_AUDIENCE", "")
    zitadel_operator_jwks_url: str = os.getenv("ZITADEL_OPERATOR_JWKS_URL", "")
    zitadel_operator_client_id: str = os.getenv("ZITADEL_OPERATOR_CLIENT_ID", "")

    zitadel_explorer_issuer: str = os.getenv("ZITADEL_EXPLORER_ISSUER", "")
    zitadel_explorer_audience: str = os.getenv("ZITADEL_EXPLORER_AUDIENCE", "")
    zitadel_explorer_jwks_url: str = os.getenv("ZITADEL_EXPLORER_JWKS_URL", "")
    zitadel_explorer_client_id: str = os.getenv("ZITADEL_EXPLORER_CLIENT_ID", "")

    internal_service_issuer: str = os.getenv("INTERNAL_SERVICE_ISSUER", "")
    internal_service_audience: str = os.getenv("INTERNAL_SERVICE_AUDIENCE", "")
    internal_service_jwks_url: str = os.getenv("INTERNAL_SERVICE_JWKS_URL", "")
    internal_service_client_id: str = os.getenv("INTERNAL_SERVICE_CLIENT_ID", "")

    # AWS S3 configuration
    gcp_access_key_id: str = os.getenv("GCP_ACCESS_KEY_ID", "")
    gcp_secret_access_key: str = os.getenv("GCP_SECRET_ACCESS_KEY", "")
    gcp_region: str = os.getenv("GCP_REGION", "us-east-1")
    gcp_s3_bucket_name: str = os.getenv("GCP_S3_BUCKET_NAME", "")
    gcp_endpoint_url: str = os.getenv("GCP_ENDPOINT_URL", "")

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
                "client_id": self.zitadel_operator_client_id,
            },
            "explorer_app": {
                "issuer": self.zitadel_explorer_issuer,
                "audience": self.zitadel_explorer_audience,
                "jwks_url": self.zitadel_explorer_jwks_url,
                "client_id": self.zitadel_explorer_client_id,
            },
            "internal_service": {
                "issuer": self.internal_service_issuer,
                "audience": self.internal_service_audience,
                "jwks_url": self.internal_service_jwks_url,
                "client_id": self.internal_service_client_id,
            },
        }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
