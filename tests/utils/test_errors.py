import pytest
from flask import Flask
from app.utils.errors import (
    AppError,
    ValidationError,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
    ForbiddenError,
    register_error_handlers,
    handle_controller_errors,
)
from sqlalchemy.exc import IntegrityError, DataError


@pytest.fixture
def error_app():
    app = Flask(__name__)
    register_error_handlers(app)

    @app.route("/validation")
    def validation_error():
        raise ValidationError("Invalid input", "email")

    @app.route("/not-found")
    def not_found_error():
        raise NotFoundError("User", "123")

    @app.route("/conflict")
    def conflict_error():
        raise ConflictError("Resource exists", "user")

    @app.route("/unauthorized")
    def unauthorized_error():
        raise UnauthorizedError()

    @app.route("/forbidden")
    def forbidden_error():
        raise ForbiddenError()

    @app.route("/server-error")
    def server_error():
        raise Exception("Internal error")

    return app


def test_validation_error(error_app):
    client = error_app.test_client()
    response = client.get("/validation")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Invalid input" in data["error"]["message"]


def test_not_found_error(error_app):
    client = error_app.test_client()
    response = client.get("/not-found")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert "not found" in data["error"]["message"]


def test_conflict_error(error_app):
    client = error_app.test_client()
    response = client.get("/conflict")
    assert response.status_code == 409
    data = response.get_json()
    assert data["success"] is False


def test_unauthorized_error(error_app):
    client = error_app.test_client()
    response = client.get("/unauthorized")
    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False


def test_forbidden_error(error_app):
    client = error_app.test_client()
    response = client.get("/forbidden")
    assert response.status_code == 403
    data = response.get_json()
    assert data["success"] is False


def test_404_handler(error_app):
    client = error_app.test_client()
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_500_handler(error_app):
    client = error_app.test_client()
    response = client.get("/server-error")
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data


def test_handle_controller_errors_integrity_duplicate():
    from flask import Flask

    app = Flask(__name__)

    with app.app_context():

        @handle_controller_errors
        def test_func():
            raise IntegrityError("statement", "params", "Duplicate entry")

        with pytest.raises(ConflictError):
            test_func()


def test_handle_controller_errors_integrity_foreign_key():
    from flask import Flask

    app = Flask(__name__)

    with app.app_context():

        @handle_controller_errors
        def test_func():
            raise IntegrityError("statement", "params", "FOREIGN KEY constraint failed")

        with pytest.raises(ValidationError):
            test_func()


def test_handle_controller_errors_integrity_other():
    from flask import Flask

    app = Flask(__name__)

    with app.app_context():

        @handle_controller_errors
        def test_func():
            raise IntegrityError("statement", "params", "other error")

        with pytest.raises(AppError):
            test_func()


def test_handle_controller_errors_data_error():
    from flask import Flask

    app = Flask(__name__)

    with app.app_context():

        @handle_controller_errors
        def test_func():
            raise DataError("statement", "params", "orig")

        with pytest.raises(ValidationError):
            test_func()


def test_handle_controller_errors_sqlalchemy_error():
    from flask import Flask
    from sqlalchemy.exc import SQLAlchemyError

    app = Flask(__name__)

    with app.app_context():

        @handle_controller_errors
        def test_func():
            raise SQLAlchemyError("Database error")

        with pytest.raises(AppError):
            test_func()
