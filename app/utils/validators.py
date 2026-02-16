"""Request validation utilities."""

import json
from functools import wraps
from typing import Any, Callable, Type

import jwt
from flask import current_app, g, request
from pydantic import BaseModel, ValidationError as PydanticValidationError

from app.utils.errors import UnauthorizedError, ValidationError
from app.utils.security import decode_token


def validate_json(schema: Type[BaseModel]) -> Callable[..., Any]:
    """Decorator to validate JSON request body against Pydantic schema."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not request.is_json:
                raise ValidationError("Content-Type must be application/json")

            try:
                data = request.get_json()
                if data is None:
                    raise ValidationError("Request body must contain valid JSON")

                validated = schema(**data)
                g.validated_json = validated.model_dump()

            except PydanticValidationError as e:
                errors = []
                for error in e.errors():
                    field = ".".join(str(loc) for loc in error["loc"])
                    errors.append(f"{field}: {error['msg']}")
                raise ValidationError("; ".join(errors))
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON format")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_query_params(schema: Type[BaseModel]) -> Callable[..., Any]:
    """Decorator to validate query parameters against Pydantic schema."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                validated = schema(**request.args.to_dict())
                g.validated_params = validated.model_dump()

            except PydanticValidationError as e:
                errors = []
                for error in e.errors():
                    field = ".".join(str(loc) for loc in error["loc"])
                    errors.append(f"{field}: {error['msg']}")
                raise ValidationError("; ".join(errors))

            return func(*args, **kwargs)

        return wrapper

    return decorator


def has_permission() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to validate JWT token and extract partner information."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise UnauthorizedError("Missing or invalid authorization header")

            token = auth_header.split(" ")[1]

            try:
                payload = decode_token(token, current_app.config["JWT_SECRET_KEY"])
                g.partner_id = payload.get("partner_id")
                g.token = token

            except jwt.ExpiredSignatureError:
                raise UnauthorizedError("Token has expired")
            except jwt.InvalidTokenError:
                raise UnauthorizedError("Invalid token")

            return func(*args, **kwargs)

        return wrapper

    return decorator
