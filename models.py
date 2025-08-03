from sqlalchemy import Column, Integer, String, Float

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    market_description = Column(String, nullable=False)
    tam_estimate = Column(Integer, nullable=False)
    growth_rate = Column(Float, nullable=False)
    consumer_insight = Column(String, nullable=False)
    hypothesis = Column(String, nullable=False)
