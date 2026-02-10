import pytest
import os
import secrets
from app.config import Config, get_settings, _get_or_generate_secret


def test_config_defaults():
    config = Config()
    assert config.DATABASE_HOST == "localhost"
    assert config.DATABASE_PORT == 3306
    assert config.DATABASE_NAME == "ceremo_db"
    assert config.JWT_EXPIRATION_HOURS == 24
    assert config.REFRESH_TOKEN_EXPIRATION_HOURS == 720
    assert config.MIN_PASSWORD_LENGTH == 8
    assert config.REMEMBER_ME_MULTIPLIER == 24
    assert config.GEOCODING_COUNTRY == "India"
    assert config.GEOCODING_COUNTRY_CODE == "in"
    assert config.GEOCODING_RESULT_LIMIT == 10


def test_config_database_url():
    config = Config(
        DATABASE_HOST="testhost",
        DATABASE_PORT=3307,
        DATABASE_USER="testuser",
        DATABASE_PASSWORD="testpass",
        DATABASE_NAME="testdb",
    )
    expected = "mysql+pymysql://testuser:testpass@testhost:3307/testdb"
    assert config.DATABASE_URL == expected


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_HOST", "envhost")
    monkeypatch.setenv("DATABASE_PORT", "3308")
    monkeypatch.setenv("JWT_EXPIRATION_HOURS", "48")
    monkeypatch.setenv("MIN_PASSWORD_LENGTH", "10")

    from importlib import reload
    import app.config

    reload(app.config)

    config = app.config.Config()
    assert config.DATABASE_HOST == "envhost"
    assert config.DATABASE_PORT == 3308
    assert config.JWT_EXPIRATION_HOURS == 48
    assert config.MIN_PASSWORD_LENGTH == 10


def test_get_settings():
    from importlib import reload
    import app.config

    reload(app.config)
    settings = app.config.get_settings()
    assert isinstance(settings, app.config.Config)


def test_get_or_generate_secret_from_env(monkeypatch):
    monkeypatch.setenv("TEST_SECRET", "my-secure-secret-key-at-least-32-chars")
    secret = _get_or_generate_secret("TEST_SECRET")
    assert secret == "my-secure-secret-key-at-least-32-chars"


def test_get_or_generate_secret_generates_in_dev(monkeypatch):
    monkeypatch.delenv("TEST_SECRET", raising=False)
    monkeypatch.setenv("ENVIRONMENT", "development")
    secret = _get_or_generate_secret("TEST_SECRET")
    assert len(secret) >= 32


def test_get_or_generate_secret_raises_in_production(monkeypatch):
    monkeypatch.delenv("TEST_SECRET", raising=False)
    monkeypatch.setenv("ENVIRONMENT", "production")

    with pytest.raises(ValueError, match="must be set in production"):
        _get_or_generate_secret("TEST_SECRET")


def test_get_or_generate_secret_short_key_in_production(monkeypatch):
    monkeypatch.setenv("TEST_SECRET", "short")
    monkeypatch.setenv("ENVIRONMENT", "production")

    with pytest.raises(ValueError, match="must be set in production"):
        _get_or_generate_secret("TEST_SECRET")
