import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock
from app.repositories.blacklisted_token_repository import BlacklistedTokenRepository
from app.models.blacklisted_token import BlacklistedToken


@pytest.fixture
def repository():
    return BlacklistedTokenRepository()


def test_is_blacklisted_true(repository, mocker):
    mock_query = mocker.patch(
        "app.repositories.blacklisted_token_repository.db.session.query"
    )
    mock_token = Mock(spec=BlacklistedToken)
    mock_query.return_value.filter_by.return_value.filter.return_value.first.return_value = (
        mock_token
    )

    result = repository.is_blacklisted("test_token")
    assert result is True


def test_is_blacklisted_false(repository, mocker):
    mock_query = mocker.patch(
        "app.repositories.blacklisted_token_repository.db.session.query"
    )
    mock_query.return_value.filter_by.return_value.filter.return_value.first.return_value = (
        None
    )

    result = repository.is_blacklisted("test_token")
    assert result is False


def test_blacklist_token(repository, mocker):
    mock_session = mocker.patch(
        "app.repositories.blacklisted_token_repository.db.session"
    )
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    token = repository.blacklist("test_token", expires_at)

    assert token.token == "test_token"
    assert token.expires_at == expires_at
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
