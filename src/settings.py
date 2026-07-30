from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    ENCRYPTION_KEY: str
    REDIS_URL: str
    REGISTRATION_MAX_ATTEMPS: int = 5

    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    def require_smtp_host(self) -> str:
        if not self.SMTP_HOST:
            raise ValueError("SMTP_HOST is not configured")
        return self.SMTP_HOST

    def require_smtp_user(self) -> str:
        if not self.SMTP_USER:
            raise ValueError("SMTP_USER is not configured")
        return self.SMTP_USER

    def require_smtp_password(self) -> str:
        if not self.SMTP_PASSWORD:
            raise ValueError("SMTP_PASSWORD is not configured")
        return self.SMTP_PASSWORD


settings = Settings() # type: ignore[call-arg]

