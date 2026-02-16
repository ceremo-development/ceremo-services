import pytest
import json
import jwt
from flask import Flask, g
from pydantic import BaseModel
from app.utils.validators import validate_json, validate_query_params, has_permission
from app.utils.errors import ValidationError, UnauthorizedError, register_error_handlers


class SampleSchema(BaseModel):
    name: str
    age: int


class QuerySchema(BaseModel):
    q: str


@pytest.fixture
def test_app():
    app = Flask(__name__)
    register_error_handlers(app)

    @app.route("/test", methods=["POST"])
    @validate_json(SampleSchema)
    def test_route():
        return {"data": g.validated_json}, 200

    @app.route("/search", methods=["GET"])
    @validate_query_params(QuerySchema)
    def search_route():
        return {"data": g.validated_params}, 200

    return app


def test_validate_json_success(test_app):
    client = test_app.test_client()
    response = client.post(
        "/test", json={"name": "John", "age": 30}, content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["name"] == "John"
    assert data["data"]["age"] == 30


def test_validate_json_missing_field(test_app):
    client = test_app.test_client()
    response = client.post(
        "/test", json={"name": "John"}, content_type="application/json"
    )
    assert response.status_code == 400


def test_validate_json_invalid_type(test_app):
    client = test_app.test_client()
    response = client.post(
        "/test",
        json={"name": "John", "age": "invalid"},
        content_type="application/json",
    )
    assert response.status_code == 400


def test_validate_json_not_json(test_app):
    client = test_app.test_client()
    response = client.post("/test", data="not json", content_type="text/plain")
    assert response.status_code == 400


def test_validate_json_empty_body(test_app):
    client = test_app.test_client()
    response = client.post("/test", data="", content_type="application/json")
    assert response.status_code == 400


def test_validate_json_null_body(test_app):
    client = test_app.test_client()
    response = client.post("/test", data="null", content_type="application/json")
    assert response.status_code == 400


def test_validate_json_malformed_json(test_app):
    client = test_app.test_client()
    response = client.post(
        "/test", data="{invalid json}", content_type="application/json"
    )
    assert response.status_code == 400


def test_validate_query_params_success(test_app):
    client = test_app.test_client()
    response = client.get("/search?q=test")
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["q"] == "test"


def test_validate_query_params_missing_field(test_app):
    client = test_app.test_client()
    response = client.get("/search")
    assert response.status_code == 400


@pytest.fixture
def auth_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret-key-at-least-32-chars-long"
    app.config["TESTING"] = True
    register_error_handlers(app)

    @app.route("/protected", methods=["GET"])
    @has_permission()
    def protected_route():
        return {"partner_id": g.partner_id}, 200

    return app


def test_has_permission_success(auth_app):
    client = auth_app.test_client()
    payload = {"partner_id": "test-partner-id", "exp": 9999999999, "iat": 1234567890}
    token = jwt.encode(
        payload, "test-secret-key-at-least-32-chars-long", algorithm="HS256"
    )

    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.get_json()
    assert data["partner_id"] == "test-partner-id"


def test_has_permission_missing_header(auth_app):
    client = auth_app.test_client()
    response = client.get("/protected")
    assert response.status_code == 401


def test_has_permission_invalid_header_format(auth_app):
    client = auth_app.test_client()
    response = client.get("/protected", headers={"Authorization": "InvalidFormat"})
    assert response.status_code == 401


def test_has_permission_expired_token(auth_app):
    client = auth_app.test_client()
    payload = {"partner_id": "test-partner-id", "exp": 1234567890, "iat": 1234567890}
    token = jwt.encode(
        payload, "test-secret-key-at-least-32-chars-long", algorithm="HS256"
    )

    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401


def test_has_permission_invalid_token(auth_app):
    client = auth_app.test_client()
    response = client.get(
        "/protected", headers={"Authorization": "Bearer invalid.token.here"}
    )

    assert response.status_code == 401
