import pytest
from app.contracts.auth_contracts import (
    SignInRequest,
    SignUpRequest,
    UserData,
    AuthData,
    AuthResponse,
    SignOutResponse,
)


def test_sign_in_request_valid():
    request = SignInRequest(
        email="test@example.com", password="password123", rememberMe=False
    )
    assert request.email == "test@example.com"
    assert request.password == "password123"
    assert request.rememberMe is False


def test_sign_up_request_valid():
    request = SignUpRequest(
        email="test@example.com",
        password="password123",
        confirmPassword="password123",
        firstName="John",
        lastName="Doe",
        phone="1234567890",
        agreeToTerms=True,
    )
    assert request.email == "test@example.com"
    assert request.firstName == "John"
    assert request.agreeToTerms is True


def test_user_data_valid():
    user = UserData(
        id="test-id",
        email="test@example.com",
        firstName="John",
        lastName="Doe",
        phone="1234567890",
    )
    assert user.id == "test-id"
    assert user.email == "test@example.com"


def test_auth_data_valid():
    user = UserData(
        id="test-id",
        email="test@example.com",
        firstName="John",
        lastName="Doe",
        phone="1234567890",
    )
    auth = AuthData(user=user, token="jwt.token", refreshToken="refresh.token")
    assert auth.user.id == "test-id"
    assert auth.token == "jwt.token"
    assert auth.refreshToken == "refresh.token"


def test_auth_response_valid():
    user = UserData(
        id="test-id",
        email="test@example.com",
        firstName="John",
        lastName="Doe",
        phone="1234567890",
    )
    auth = AuthData(user=user, token="jwt.token", refreshToken="refresh.token")
    response = AuthResponse(data=auth, message="Success")
    assert response.success is True
    assert response.message == "Success"


def test_sign_out_response_valid():
    response = SignOutResponse(message="Sign out successful")
    assert response.success is True
    assert response.message == "Sign out successful"
