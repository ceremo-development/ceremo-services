"""Serialization utilities for request/response transformation."""

import re
from functools import wraps
from typing import Dict, Any, Callable

from flask import g
from marshmallow import Schema


class CamelCaseSchema(Schema):
    def _camel_to_snake(self, name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def _convert_camel_case_keys(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {self._camel_to_snake(k): v for k, v in data.items()}

    def load(self, data: Any, **kwargs: Any) -> Any:
        if isinstance(data, dict):
            data = self._convert_camel_case_keys(data)
        return super().load(data, **kwargs)


def transform_camel_case(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if hasattr(g, "validated_json"):
            schema = CamelCaseSchema()
            g.validated_json = schema._convert_camel_case_keys(g.validated_json)
        return func(*args, **kwargs)

    return wrapper
