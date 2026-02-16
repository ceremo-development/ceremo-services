"""Blacklisted Token repository."""

from datetime import datetime, timezone
from app.models.blacklisted_token import BlacklistedToken
from app.models.base import db


class BlacklistedTokenRepository:
    """Repository for blacklisted token data access."""

    def is_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted."""
        return (
            db.session.query(BlacklistedToken)
            .filter_by(token=token)
            .filter(BlacklistedToken.expires_at > datetime.now(timezone.utc))
            .first()
            is not None
        )

    def blacklist(self, token: str, expires_at: datetime) -> BlacklistedToken:
        """Add token to blacklist."""
        blacklisted = BlacklistedToken(token=token, expires_at=expires_at)
        db.session.add(blacklisted)
        db.session.commit()
        return blacklisted
