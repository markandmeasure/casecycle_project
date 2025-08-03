from sqlalchemy import Column, Integer, String, Float

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    token = Column(String, nullable=True)


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    market_description = Column(String, nullable=True)
    tam_estimate = Column(Float, nullable=True)
    growth_rate = Column(Float, nullable=True)
    consumer_insight = Column(String, nullable=True)
    hypothesis = Column(String, nullable=True)
