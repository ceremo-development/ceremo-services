import pytest
from unittest.mock import Mock
from flask import Flask
from app.routes.location_routes import create_location_routes
from app.contracts.location_contracts import LocationSearchResponse, LocationData
from app.utils.errors import register_error_handlers


@pytest.fixture
def mock_location_service():
    return Mock()


@pytest.fixture
def location_client(mock_location_service):
    app = Flask(__name__)
    app.config["TESTING"] = True
    register_error_handlers(app)
    location_bp = create_location_routes(mock_location_service)
    app.register_blueprint(location_bp, url_prefix="/api/locations")
    return app.test_client(), mock_location_service


def test_search_locations_success(location_client):
    client, mock_service = location_client
    location_data = LocationData(
        id="test-id",
        pincode="560001",
        city="Bangalore",
        state="Karnataka",
        district="Bangalore Urban",
        area="MG Road",
    )
    mock_service.search_locations.return_value = LocationSearchResponse(
        data=[location_data], message="Locations found"
    )

    response = client.get("/api/locations/search?q=Bangalore")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["data"]) == 1
    assert data["data"][0]["city"] == "Bangalore"
    mock_service.search_locations.assert_called_once_with("Bangalore")
