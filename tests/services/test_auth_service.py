import pytest
from unittest.mock import Mock
from app.services.auth_service import AuthService
from app.models.rental_partner import RentalPartner
from app.utils.errors import ValidationError, UnauthorizedError, ConflictError


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def mock_blacklist_repo():
    return Mock()


@pytest.fixture
def mock_profile_repo():
    return Mock()


@pytest.fixture
def auth_service(mock_repository, mock_blacklist_repo, mock_profile_repo):
    return AuthService(
        repository=mock_repository,
        blacklist_repo=mock_blacklist_repo,
        profile_repo=mock_profile_repo,
        jwt_secret="test-secret-key-at-least-32-chars-long-for-security",
        jwt_expiration=24,
        refresh_expiration=720,
        min_password_length=8,
        remember_me_multiplier=24,
    )


@pytest.fixture
def mock_partner():
    partner = Mock(spec=RentalPartner)
    partner.id = "test-id"
    partner.email = "test@example.com"
    partner.first_name = "John"
    partner.last_name = "Doe"
    partner.phone = "1234567890"
    partner.password_hash = "$2b$12$test_hash"
    return partner


def test_sign_up_success(
    auth_service, mock_repository, mock_profile_repo, mock_partner
):
    mock_repository.find_by_email.return_value = None
    mock_repository.create.return_value = mock_partner
    mock_profile_repo.create.return_value = Mock()

    response = auth_service.sign_up(
        email="test@example.com",
        password="password123",
        confirm_password="password123",
        first_name="John",
        last_name="Doe",
        phone="1234567890",
        agree_to_terms=True,
    )

    assert response.success is True
    assert response.data.user.email == "test@example.com"
    assert response.data.token is not None
    assert response.data.refreshToken is not None
    mock_profile_repo.create.assert_called_once()


def test_sign_up_terms_not_agreed(auth_service):
    with pytest.raises(ValidationError, match="agree to terms"):
        auth_service.sign_up(
            email="test@example.com",
            password="password123",
            confirm_password="password123",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            agree_to_terms=False,
        )


def test_sign_up_password_mismatch(auth_service):
    with pytest.raises(ValidationError, match="do not match"):
        auth_service.sign_up(
            email="test@example.com",
            password="password123",
            confirm_password="different",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            agree_to_terms=True,
        )


def test_sign_up_password_too_short(auth_service):
    with pytest.raises(ValidationError, match="at least 8"):
        auth_service.sign_up(
            email="test@example.com",
            password="short",
            confirm_password="short",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            agree_to_terms=True,
        )


def test_sign_up_email_exists(auth_service, mock_repository, mock_partner):
    mock_repository.find_by_email.return_value = mock_partner

    with pytest.raises(ConflictError, match="already exists"):
        auth_service.sign_up(
            email="test@example.com",
            password="password123",
            confirm_password="password123",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            agree_to_terms=True,
        )


def test_sign_in_success(auth_service, mock_repository, mock_partner, mocker):
    mock_repository.find_by_email.return_value = mock_partner
    mocker.patch("app.services.auth_service.verify_password", return_value=True)

    response = auth_service.sign_in(
        email="test@example.com", password="password123", remember_me=False
    )

    assert response.success is True
    assert response.data.user.email == "test@example.com"


def test_sign_in_invalid_email(auth_service, mock_repository):
    mock_repository.find_by_email.return_value = None

    with pytest.raises(UnauthorizedError, match="Invalid email or password"):
        auth_service.sign_in(
            email="wrong@example.com", password="password123", remember_me=False
        )


def test_sign_in_invalid_password(auth_service, mock_repository, mock_partner, mocker):
    mock_repository.find_by_email.return_value = mock_partner
    mocker.patch("app.services.auth_service.verify_password", return_value=False)

    with pytest.raises(UnauthorizedError, match="Invalid email or password"):
        auth_service.sign_in(
            email="test@example.com", password="wrong", remember_me=False
        )


def test_sign_in_remember_me(auth_service, mock_repository, mock_partner, mocker):
    mock_repository.find_by_email.return_value = mock_partner
    mocker.patch("app.services.auth_service.verify_password", return_value=True)
    mock_generate = mocker.patch(
        "app.services.auth_service.generate_token", return_value="token"
    )

    auth_service.sign_in(
        email="test@example.com", password="password123", remember_me=True
    )

    assert mock_generate.call_args_list[0][0][2] == 24 * 24


def test_sign_out_success(auth_service, mock_blacklist_repo, mocker):
    token = "valid.jwt.token"
    mock_decode = mocker.patch(
        "app.services.auth_service.decode_token",
        return_value={"partner_id": "test-id", "exp": 1234567890},
    )
    mock_blacklist_repo.blacklist.return_value = Mock()

    response = auth_service.sign_out(token)

    assert response.success is True
    assert response.message == "Sign out successful"
    mock_decode.assert_called_once_with(token, auth_service.jwt_secret)
    mock_blacklist_repo.blacklist.assert_called_once()


def test_sign_out_expired_token(auth_service, mocker):
    import jwt as pyjwt

    token = "expired.jwt.token"
    mocker.patch(
        "app.services.auth_service.decode_token",
        side_effect=pyjwt.ExpiredSignatureError,
    )

    with pytest.raises(UnauthorizedError, match="Token has expired"):
        auth_service.sign_out(token)


def test_sign_out_invalid_token(auth_service, mocker):
    import jwt as pyjwt

    token = "invalid.jwt.token"
    mocker.patch(
        "app.services.auth_service.decode_token", side_effect=pyjwt.InvalidTokenError
    )

    with pytest.raises(UnauthorizedError, match="Invalid token"):
        auth_service.sign_out(token)
