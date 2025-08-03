"""Populate database with sample data in an idempotent way.

Running this script multiple times will not create duplicate
``Opportunity`` records. Each opportunity is looked up by its title
before insertion and updated in place if it already exists.
"""

from typing import List, Dict

from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)


def _upsert_opportunity(session: Session, data: Dict) -> None:
    """Insert or update an opportunity based on its title.

    ``session.merge`` attaches the object to the current session and performs
    an update if it already exists; otherwise it inserts a new row.
    """
    existing = session.query(models.Opportunity).filter_by(title=data["title"]).one_or_none()
    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        session.merge(existing)
    else:
        session.merge(models.Opportunity(**data))


def populate() -> None:
    """Populate the database with a fixed set of opportunities.

    Because each record is upserted by title, re-running this function is safe
    and will not result in duplicate rows or integrity errors.
    """
    session: Session = SessionLocal()
    try:
        # Ensure a default user exists
        user = session.query(models.User).filter_by(name="Sample User").one_or_none()
        if not user:
            user = models.User(name="Sample User")
            session.add(user)
            session.commit()
            session.refresh(user)

        sample_opportunities: List[Dict] = [
            {
                "title": "Eco-Friendly Water Bottle",
                "market_description": "Reusable bottle market",
                "tam_estimate": 1_200_000,
                "growth_rate": 7.5,
                "consumer_insight": "Consumers seek sustainable alternatives",
                "hypothesis": "A durable bottle with filter will attract buyers",
                "user_id": user.id,
            },
            {
                "title": "Smart Home Energy Monitor",
                "market_description": "Devices that track household energy usage",
                "tam_estimate": 2_000_000,
                "growth_rate": 10.0,
                "consumer_insight": "People want to reduce energy bills",
                "hypothesis": "Real-time usage alerts can save cost",
                "user_id": user.id,
            },
        ]

        for opp in sample_opportunities:
            _upsert_opportunity(session, opp)

        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    populate()
