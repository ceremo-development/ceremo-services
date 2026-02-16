import pytest
from unittest.mock import Mock
from flask import Flask
from app.routes.partner_profile_routes import create_partner_profile_routes
from app.contracts.partner_profile_contracts import (
    PartnerProfileResponse,
    PartnerProfileData,
)
from app.utils.errors import register_error_handlers


@pytest.fixture
def mock_profile_service():
    return Mock()


@pytest.fixture
def profile_client(mock_profile_service):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret-key-at-least-32-chars-long"
    app.config["TESTING"] = True
    register_error_handlers(app)
    profile_bp = create_partner_profile_routes(mock_profile_service)
    app.register_blueprint(profile_bp, url_prefix="/api/partner")
    return app.test_client(), mock_profile_service


def test_get_profile_success(profile_client, mocker):
    client, mock_service = profile_client
    mocker.patch(
        "app.utils.validators.decode_token",
        return_value={"partner_id": "test-partner-id", "exp": 9999999999},
    )

    profile_data = PartnerProfileData(
        id="profile-id",
        partnerId="test-partner-id",
        businessName="Test Business",
        ownerName="John Doe",
        email="test@example.com",
        phone="1234567890",
        address="123 Test St",
        city="Test City",
        state="Test State",
        pincode="123456",
        businessType="Rental",
        yearsInBusiness="5",
        description="Test description",
        categories=["Category1"],
        serviceAreas=["Area1"],
        deliveryRadius="10",
    )
    mock_service.get_profile.return_value = PartnerProfileResponse(
        data=profile_data, message="Profile fetched"
    )

    response = client.get(
        "/api/partner/profile",
        headers={"Authorization": "Bearer valid.jwt.token"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["businessName"] == "Test Business"


def test_update_profile_success(profile_client, mocker):
    client, mock_service = profile_client
    mocker.patch(
        "app.utils.validators.decode_token",
        return_value={"partner_id": "test-partner-id", "exp": 9999999999},
    )

    profile_data = PartnerProfileData(
        id="profile-id",
        partnerId="test-partner-id",
        businessName="Updated Business",
        ownerName="Jane Doe",
        email="updated@example.com",
        phone="0987654321",
        address="456 New St",
        city="New City",
        state="New State",
        pincode="654321",
        businessType="Service",
        yearsInBusiness="10",
        description="Updated description",
        categories=["Category2"],
        serviceAreas=["Area2"],
        deliveryRadius="20",
    )
    mock_service.update_profile.return_value = PartnerProfileResponse(
        data=profile_data, message="Profile updated"
    )

    response = client.put(
        "/api/partner/profile",
        headers={"Authorization": "Bearer valid.jwt.token"},
        json={
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
        },
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["businessName"] == "Updated Business"
