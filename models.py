from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=True)

    opportunities = relationship("Opportunity", back_populates="user")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    market_description = Column(String, nullable=True)
    tam_estimate = Column(Float, nullable=True)
    growth_rate = Column(Float, nullable=True)
    consumer_insight = Column(String, nullable=True)
    hypothesis = Column(String, nullable=True)

    user = relationship("User", back_populates="opportunities")
