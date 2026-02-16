import pytest
from unittest.mock import Mock
from app.repositories.location_repository import LocationRepository
from app.models.location import Location


@pytest.fixture
def repository():
    return LocationRepository()


@pytest.fixture
def mock_location():
    location = Mock(spec=Location)
    location.id = "test-id"
    location.pincode = "560001"
    location.city = "Bangalore"
    location.state = "Karnataka"
    location.district = "Bangalore Urban"
    location.area = "MG Road"
    return location


def test_search_locations(repository, mock_location, mocker):
    mock_query = mocker.patch("app.repositories.location_repository.db.session.query")
    mock_query.return_value.filter.return_value.limit.return_value.all.return_value = [
        mock_location
    ]

    results = repository.search_locations("Bangalore")
    assert len(results) == 1
    assert results[0].city == "Bangalore"


def test_bulk_create_new_locations(repository, mocker):
    mock_session = mocker.patch("app.repositories.location_repository.db.session")
    mock_query = mocker.patch("app.repositories.location_repository.db.session.query")
    mock_query.return_value.filter_by.return_value.first.return_value = None

    locations_data = [
        {
            "pincode": "560001",
            "city": "Bangalore",
            "area": "MG Road",
            "state": "Karnataka",
            "district": "Bangalore Urban",
        }
    ]
    results = repository.bulk_create(locations_data)

    assert len(results) == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_bulk_create_existing_location(repository, mock_location, mocker):
    mock_session = mocker.patch("app.repositories.location_repository.db.session")
    mock_query = mocker.patch("app.repositories.location_repository.db.session.query")
    mock_query.return_value.filter_by.return_value.first.return_value = mock_location

    locations_data = [
        {
            "pincode": "560001",
            "city": "Bangalore",
            "area": "MG Road",
            "state": "Karnataka",
            "district": "Bangalore Urban",
        }
    ]
    results = repository.bulk_create(locations_data)

    assert len(results) == 0
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
