import pytest
from unittest.mock import Mock
from app.repositories.partner_profile_repository import PartnerProfileRepository
from app.models.partner_profile import PartnerProfile


@pytest.fixture
def repository():
    return PartnerProfileRepository()


@pytest.fixture
def mock_profile():
    profile = Mock(spec=PartnerProfile)
    profile.id = "profile-id"
    profile.partner_id = "partner-id"
    profile.business_name = "Test Business"
    profile.owner_name = "John Doe"
    profile.email = "test@example.com"
    profile.phone = "1234567890"
    profile.address = "123 Test St"
    profile.city = "Test City"
    profile.state = "Test State"
    profile.pincode = "123456"
    profile.business_type = "Rental"
    profile.years_in_business = "5"
    profile.description = "Test description"
    profile.categories = ["Category1"]
    profile.service_areas = ["Area1"]
    profile.delivery_radius = "10"
    return profile


def test_get_by_partner_id(repository, mock_profile, mocker):
    mock_query = mocker.patch(
        "app.repositories.partner_profile_repository.db.session.query"
    )
    mock_query.return_value.filter_by.return_value.first.return_value = mock_profile

    profile = repository.get_by_partner_id("partner-id")
    assert profile.partner_id == "partner-id"


def test_create(repository, mocker):
    mock_session = mocker.patch(
        "app.repositories.partner_profile_repository.db.session"
    )

    profile = repository.create(
        partner_id="partner-id",
        business_name="Test Business",
        owner_name="John Doe",
        email="test@example.com",
        phone="1234567890",
        address="123 Test St",
        city="Test City",
        state="Test State",
        pincode="123456",
        business_type="Rental",
        years_in_business="5",
        description="Test description",
        categories=["Category1"],
        service_areas=["Area1"],
        delivery_radius="10",
    )

    assert profile.business_name == "Test Business"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_update(repository, mock_profile, mocker):
    mock_session = mocker.patch(
        "app.repositories.partner_profile_repository.db.session"
    )
    mocker.patch.object(repository, "get_by_partner_id", return_value=mock_profile)

    profile = repository.update(
        partner_id="partner-id",
        business_name="Updated Business",
        owner_name="Jane Doe",
        email="updated@example.com",
        phone="0987654321",
        address="456 New St",
        city="New City",
        state="New State",
        pincode="654321",
        business_type="Service",
        years_in_business="10",
        description="Updated description",
        categories=["Category2"],
        service_areas=["Area2"],
        delivery_radius="20",
    )

    assert profile.business_name == "Updated Business"
    mock_session.commit.assert_called_once()


def test_update_not_found(repository, mocker):
    mocker.patch("app.repositories.partner_profile_repository.db.session")
    mocker.patch.object(repository, "get_by_partner_id", return_value=None)

    with pytest.raises(ValueError, match="Profile not found for partner_id"):
        repository.update(
            partner_id="nonexistent-id",
            business_name="Updated Business",
            owner_name="Jane Doe",
            email="updated@example.com",
            phone="0987654321",
            address="456 New St",
            city="New City",
            state="New State",
            pincode="654321",
            business_type="Service",
            years_in_business="10",
            description="Updated description",
            categories=["Category2"],
            service_areas=["Area2"],
            delivery_radius="20",
        )
