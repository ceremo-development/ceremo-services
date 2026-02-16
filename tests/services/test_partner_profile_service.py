import pytest
from unittest.mock import Mock
from app.services.partner_profile_service import PartnerProfileService
from app.models.partner_profile import PartnerProfile
from app.models.rental_partner import RentalPartner
from app.utils.errors import NotFoundError


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def mock_partner_repository():
    return Mock()


@pytest.fixture
def profile_service(mock_repository, mock_partner_repository):
    return PartnerProfileService(mock_repository, mock_partner_repository)


@pytest.fixture
def mock_partner():
    partner = Mock(spec=RentalPartner)
    partner.id = "partner-id"
    partner.email = "test@example.com"
    partner.first_name = "John"
    partner.last_name = "Doe"
    partner.phone = "1234567890"
    return partner


@pytest.fixture
def mock_profile():
    profile = Mock(spec=PartnerProfile)
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


def test_get_profile_exists(profile_service, mock_repository, mock_profile):
    mock_repository.get_by_partner_id.return_value = mock_profile

    response = profile_service.get_profile("partner-id")

    assert response.data.businessName == "Test Business"
    assert response.message == "Profile fetched successfully"


def test_get_profile_not_exists_partner_exists(
    profile_service, mock_repository, mock_partner_repository, mock_partner
):
    mock_repository.get_by_partner_id.return_value = None
    mock_partner_repository.find_by_id.return_value = mock_partner

    response = profile_service.get_profile("partner-id")

    assert response.data.ownerName == "John Doe"
    assert response.message == "Profile not found"


def test_get_profile_partner_not_exists(
    profile_service, mock_repository, mock_partner_repository
):
    mock_repository.get_by_partner_id.return_value = None
    mock_partner_repository.find_by_id.return_value = None

    with pytest.raises(NotFoundError):
        profile_service.get_profile("partner-id")


def test_update_profile_exists(
    profile_service,
    mock_repository,
    mock_partner_repository,
    mock_partner,
    mock_profile,
):
    mock_partner_repository.find_by_id.return_value = mock_partner
    mock_repository.get_by_partner_id.return_value = mock_profile
    mock_repository.update.return_value = mock_profile

    data = {
        "businessName": "Updated Business",
        "ownerName": "Jane Doe",
        "email": "updated@example.com",
        "phone": "0987654321",
        "address": "456 New St",
        "city": "New City",
        "state": "New State",
        "pincode": "654321",
        "businessType": "Service",
        "yearsInBusiness": "10",
        "description": "Updated description",
        "categories": ["Category2"],
        "serviceAreas": ["Area2"],
        "deliveryRadius": "20",
    }

    response = profile_service.update_profile("partner-id", data)

    assert response.message == "Profile updated successfully"
    mock_repository.update.assert_called_once()


def test_update_profile_not_exists(
    profile_service,
    mock_repository,
    mock_partner_repository,
    mock_partner,
    mock_profile,
):
    mock_partner_repository.find_by_id.return_value = mock_partner
    mock_repository.get_by_partner_id.return_value = None
    mock_repository.create.return_value = mock_profile

    data = {
        "businessName": "New Business",
        "ownerName": "John Doe",
        "email": "test@example.com",
        "phone": "1234567890",
        "address": "123 Test St",
        "city": "Test City",
        "state": "Test State",
        "pincode": "123456",
        "businessType": "Rental",
        "yearsInBusiness": "5",
        "description": "Test description",
        "categories": ["Category1"],
        "serviceAreas": ["Area1"],
        "deliveryRadius": "10",
    }

    response = profile_service.update_profile("partner-id", data)

    assert response.message == "Profile updated successfully"
    mock_repository.create.assert_called_once()


def test_update_profile_partner_not_exists(profile_service, mock_partner_repository):
    mock_partner_repository.find_by_id.return_value = None

    with pytest.raises(NotFoundError):
        profile_service.update_profile("partner-id", {})
