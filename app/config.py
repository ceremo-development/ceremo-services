import os
import secrets
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _get_or_generate_secret(env_var: str, min_length: int = 32) -> str:
    """Get secret from env or generate secure random key."""
    secret = os.getenv(env_var, "")
    if not secret or len(secret) < min_length:
        env = os.getenv("ENVIRONMENT", "development")
        if env == "production":
            raise ValueError(
                f"{env_var} must be set in production environment. "
                f"Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        return secrets.token_urlsafe(min_length)
    return secret


@dataclass
class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "postgres")

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY: str = _get_or_generate_secret("SECRET_KEY")

    JWT_SECRET_KEY: str = _get_or_generate_secret("JWT_SECRET_KEY")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    REFRESH_TOKEN_EXPIRATION_HOURS: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRATION_HOURS", "720")
    )

    MIN_PASSWORD_LENGTH: int = int(os.getenv("MIN_PASSWORD_LENGTH", "8"))
    REMEMBER_ME_MULTIPLIER: int = int(os.getenv("REMEMBER_ME_MULTIPLIER", "24"))

    GEOCODING_COUNTRY: str = os.getenv("GEOCODING_COUNTRY", "India")
    GEOCODING_COUNTRY_CODE: str = os.getenv("GEOCODING_COUNTRY_CODE", "in")
    GEOCODING_RESULT_LIMIT: int = int(os.getenv("GEOCODING_RESULT_LIMIT", "10"))

    R2_ACCESS_KEY: str = os.getenv("R2_ACCESS_KEY", "")
    R2_SECRET_KEY: str = os.getenv("R2_SECRET_KEY", "")
    R2_ENDPOINT: str = os.getenv("R2_ENDPOINT", "")
    R2_BUCKET: str = os.getenv("R2_BUCKET", "")

    def get_database_url(self) -> str:
        """Get database URL from env or construct from components."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


def get_settings() -> Config:
    return Config()
