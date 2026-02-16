import pytest
from unittest.mock import Mock
from app.services.nominatim_service import NominatimService


@pytest.fixture
def nominatim_service():
    return NominatimService()


def test_search_places_success(nominatim_service, mocker):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "display_name": "Bangalore, Karnataka, India",
            "address": {
                "city": "Bangalore",
                "state": "Karnataka",
                "postcode": "560001",
                "state_district": "Bangalore Urban",
            },
        }
    ]
    mock_response.raise_for_status = Mock()
    mocker.patch("requests.get", return_value=mock_response)

    results = nominatim_service.search_places("Bangalore")

    assert len(results) == 1
    assert results[0]["city"] == "Bangalore"


def test_search_places_request_exception(nominatim_service, mocker):
    import requests

    mocker.patch("requests.get", side_effect=requests.RequestException("API error"))

    results = nominatim_service.search_places("Bangalore")

    assert results == []


def test_search_places_general_exception(nominatim_service, mocker):
    mocker.patch("requests.get", side_effect=Exception("Unexpected error"))

    results = nominatim_service.search_places("Bangalore")

    assert results == []


def test_parse_result_valid(nominatim_service):
    result = {
        "address": {
            "city": "Bangalore",
            "state": "Karnataka",
            "postcode": "560001",
            "state_district": "Bangalore Urban",
        }
    }

    parsed = nominatim_service._parse_result(result)

    assert parsed["city"] == "Bangalore"
    assert parsed["state"] == "Karnataka"
    assert parsed["pincode"] == "560001"


def test_parse_result_missing_state(nominatim_service):
    result = {"address": {"city": "Bangalore"}}

    parsed = nominatim_service._parse_result(result)

    assert parsed is None


def test_parse_result_no_pincode(nominatim_service):
    result = {"address": {"city": "Bangalore", "state": "Karnataka"}}

    parsed = nominatim_service._parse_result(result)

    assert parsed["pincode"] == "000000"


def test_parse_result_exception(nominatim_service):
    result = {}

    parsed = nominatim_service._parse_result(result)

    assert parsed is None


def test_parse_result_with_village(nominatim_service):
    result = {
        "address": {
            "village": "Test Village",
            "state": "Karnataka",
            "state_district": "Test District",
        }
    }

    parsed = nominatim_service._parse_result(result)

    assert parsed["area"] == "Test Village"
    assert parsed["city"] == "Test Village"


def test_parse_result_with_town(nominatim_service):
    result = {
        "address": {
            "town": "Test Town",
            "state": "Karnataka",
        }
    }

    parsed = nominatim_service._parse_result(result)

    assert parsed["area"] == "Test Town"
    assert parsed["city"] == "Test Town"


def test_parse_result_with_municipality(nominatim_service):
    result = {
        "address": {
            "municipality": "Test Municipality",
            "state": "Karnataka",
        }
    }

    parsed = nominatim_service._parse_result(result)

    assert parsed["area"] == "Test Municipality"
    assert parsed["city"] == "Test Municipality"
