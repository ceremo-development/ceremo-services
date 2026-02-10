import pytest
from unittest.mock import Mock
from app.repositories.rental_partner_repository import RentalPartnerRepository
from app.models.rental_partner import RentalPartner


@pytest.fixture
def repository():
    return RentalPartnerRepository()


@pytest.fixture
def mock_partner():
    partner = Mock(spec=RentalPartner)
    partner.id = "test-id"
    partner.email = "test@example.com"
    partner.first_name = "John"
    partner.last_name = "Doe"
    partner.phone = "1234567890"
    partner.password_hash = "hashed_password"
    return partner


def test_create_rental_partner(repository, mock_partner, mocker):
    mock_session = mocker.patch("app.repositories.rental_partner_repository.db.session")
    mock_session.add = Mock()
    mock_session.commit = Mock()

    partner = repository.create(
        email="test@example.com",
        password_hash="hashed_password",
        first_name="John",
        last_name="Doe",
        phone="1234567890",
    )

    assert partner.email == "test@example.com"
    assert partner.first_name == "John"
    assert partner.last_name == "Doe"
    assert partner.phone == "1234567890"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_find_by_email_exists(repository, mock_partner, mocker):
    mock_query = mocker.patch(
        "app.repositories.rental_partner_repository.db.session.query"
    )
    mock_query.return_value.filter_by.return_value.first.return_value = mock_partner

    partner = repository.find_by_email("test@example.com")
    assert partner is not None
    assert partner.email == "test@example.com"


def test_find_by_email_not_exists(repository, mocker):
    mock_query = mocker.patch(
        "app.repositories.rental_partner_repository.db.session.query"
    )
    mock_query.return_value.filter_by.return_value.first.return_value = None

    partner = repository.find_by_email("nonexistent@example.com")
    assert partner is None


def test_find_by_id_exists(repository, mock_partner, mocker):
    mock_query = mocker.patch(
        "app.repositories.rental_partner_repository.db.session.query"
    )
    mock_query.return_value.filter_by.return_value.first.return_value = mock_partner

    partner = repository.find_by_id("test-id")
    assert partner is not None
    assert partner.id == "test-id"


def test_find_by_id_not_exists(repository, mocker):
    mock_query = mocker.patch(
        "app.repositories.rental_partner_repository.db.session.query"
    )
    mock_query.return_value.filter_by.return_value.first.return_value = None

    partner = repository.find_by_id("nonexistent-id")
    assert partner is None
