import pytest
from unittest.mock import Mock
from app.services.location_service import LocationService
from app.models.location import Location
from app.utils.errors import ValidationError


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def mock_geocoding_service():
    return Mock()


@pytest.fixture
def location_service(mock_repository, mock_geocoding_service):
    return LocationService(mock_repository, mock_geocoding_service)


@pytest.fixture
def mock_location():
    location = Mock(spec=Location)
    location.pincode = "560001"
    location.city = "Bangalore"
    location.state = "Karnataka"
    location.district = "Bangalore Urban"
    location.area = "MG Road"
    return location


def test_search_locations_query_too_short(location_service):
    with pytest.raises(ValidationError, match="at least 2 characters"):
        location_service.search_locations("a")


def test_search_locations_found_in_db(location_service, mock_repository, mock_location):
    mock_repository.search_locations.return_value = [mock_location]

    response = location_service.search_locations("Bangalore")

    assert len(response.data) == 1
    assert response.data[0].city == "Bangalore"
    assert response.message == "Locations found"


def test_search_locations_not_in_db_found_in_api(
    location_service, mock_repository, mock_geocoding_service
):
    mock_repository.search_locations.return_value = []
    api_results = [
        {
            "pincode": "560001",
            "city": "Bangalore",
            "state": "Karnataka",
            "district": "Bangalore Urban",
            "area": "MG Road",
        }
    ]
    mock_geocoding_service.search_places.return_value = api_results
    mock_repository.bulk_create.return_value = []

    response = location_service.search_locations("Bangalore")

    assert len(response.data) == 1
    assert response.data[0].city == "Bangalore"
    mock_geocoding_service.search_places.assert_called_once_with("Bangalore")
    mock_repository.bulk_create.assert_called_once_with(api_results)


def test_search_locations_not_found(
    location_service, mock_repository, mock_geocoding_service
):
    mock_repository.search_locations.return_value = []
    mock_geocoding_service.search_places.return_value = []

    response = location_service.search_locations("Unknown")

    assert len(response.data) == 0
    assert response.message == "No locations found"
