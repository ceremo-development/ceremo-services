"""Rental Partner repository."""

from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.models.rental_partner import RentalPartner
from app.models.base import db


class RentalPartnerRepository:
    """Repository for rental partner data access."""

    def find_by_email(self, email: str) -> Optional[RentalPartner]:
        """Find rental partner by email."""
        return db.session.query(RentalPartner).filter_by(email=email).first()

    def find_by_id(self, partner_id: str) -> Optional[RentalPartner]:
        """Find rental partner by ID."""
        return db.session.query(RentalPartner).filter_by(id=partner_id).first()

    def create(
        self,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        phone: str,
    ) -> RentalPartner:
        """Create new rental partner."""
        partner = RentalPartner(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        db.session.add(partner)
        db.session.commit()
        return partner
