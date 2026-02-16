import pytest
import logging
from flask import Flask, g
from app.utils.logging import setup_logger, setup_request_logging, RequestFormatter


def test_request_formatter_with_request_id():
    formatter = RequestFormatter("%(request_id)s - %(message)s")
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None,
    )

    app = Flask(__name__)
    with app.app_context():
        g.request_id = "test-id-123"
        formatted = formatter.format(record)
        assert "test-id-123" in formatted


def test_request_formatter_without_request_id():
    formatter = RequestFormatter("%(request_id)s - %(message)s")
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    assert formatted is not None


def test_setup_logger():
    logger = setup_logger("test_logger")
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0


def test_setup_logger_existing_handlers():
    logger = setup_logger("test_logger_existing")
    initial_count = len(logger.handlers)
    logger2 = setup_logger("test_logger_existing")
    assert len(logger2.handlers) == initial_count


def test_setup_request_logging():
    app = Flask(__name__)
    setup_request_logging(app)

    @app.route("/test")
    def test_route():
        return {"request_id": g.request_id}

    client = app.test_client()
    response = client.get("/test")
    data = response.get_json()
    assert "request_id" in data
    assert len(data["request_id"]) > 0
