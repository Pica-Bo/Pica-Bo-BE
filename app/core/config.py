from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str = 'mongodb://mongo:27017/fastapi_app'
    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_exp_minutes: int = 60
    app_host: str = '0.0.0.0'
    app_port: int = 8000
    admin_email: str | None = None
    admin_password: str | None = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
