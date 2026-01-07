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
    # Optional admin bootstrap credentials
    admin_email: str | None = None
    admin_password: str | None = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
