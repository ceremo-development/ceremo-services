"""Blacklisted Token domain model."""

from datetime import datetime, timezone
from app.models.base import db, BaseModel


class BlacklistedToken(BaseModel):
    __tablename__ = "blacklisted_tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False, index=True)
    blacklisted_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    expires_at = db.Column(db.DateTime, nullable=False, index=True)

    __table_args__ = (db.Index("idx_blacklisted_tokens_expires_at", "expires_at"),)
