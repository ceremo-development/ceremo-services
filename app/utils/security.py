"""Security utilities for authentication."""

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    return bool(bcrypt.checkpw(password.encode(), password_hash.encode()))


def generate_token(partner_id: str, secret_key: str, expiration_hours: int) -> str:
    """Generate JWT token."""
    payload = {
        "partner_id": partner_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expiration_hours),
        "iat": datetime.now(timezone.utc),
    }
    return str(jwt.encode(payload, secret_key, algorithm="HS256"))


def decode_token(token: str, secret_key: str) -> Dict[str, Any]:
    """Decode and verify JWT token."""
    return dict(jwt.decode(token, secret_key, algorithms=["HS256"]))
