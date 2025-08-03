from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from pathlib import Path
from jinja2 import Template

import models
from database import SessionLocal, engine
from settings import ALLOWED_ORIGINS

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

TEMPLATE_PATH = Path(__file__).with_name("prompt_templates.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("ENVIRONMENT") == "development":
    from populate_sample_data import populate

    @app.on_event("startup")
    def _load_sample_data() -> None:
        populate()


@app.get("/")
def root() -> dict:
    """Basic root endpoint to confirm the API is running."""
    return {"status": "ok"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_templates() -> dict:
    if not TEMPLATE_PATH.exists():
        raise HTTPException(status_code=500, detail="Template file not found")
    with TEMPLATE_PATH.open() as f:
        return json.load(f)


class UserCreate(BaseModel):
    name: str


class UserSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class OpportunityCreate(BaseModel):
    title: str
    market_description: Optional[str] = None
    tam_estimate: Optional[float] = Field(default=None, gt=0)
    growth_rate: Optional[float] = Field(default=None, ge=0)
    consumer_insight: Optional[str] = None
    hypothesis: Optional[str] = None
    

class OpportunitySchema(OpportunityCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/opportunities/", response_model=OpportunitySchema)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    db_opportunity = models.Opportunity(**opportunity.model_dump())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


@app.get("/opportunities/", response_model=List[OpportunitySchema])
def read_opportunities(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return (
        db.query(models.Opportunity)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/prompt/{opportunity_id}")
def generate_prompt(
    opportunity_id: int, template_name: str = "default", db: Session = Depends(get_db)
):
    templates = load_templates()
    template_str = templates.get(template_name)
    if template_str is None:
        raise HTTPException(status_code=404, detail="Template not found")

    opportunity = (
        db.query(models.Opportunity)
        .filter(models.Opportunity.id == opportunity_id)
        .first()
    )
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    data = {
        "title": opportunity.title or "",
        "market_description": opportunity.market_description or "",
        "tam_estimate": opportunity.tam_estimate or "",
        "growth_rate": opportunity.growth_rate or "",
        "consumer_insight": opportunity.consumer_insight or "",
        "hypothesis": opportunity.hypothesis or "",
    }
    prompt = Template(template_str).render(**data)
    return {"prompt": prompt}


@app.get("/healthcheck")
def healthcheck():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unavailable")
    finally:
        db.close()
    return {"status": "ok"}
