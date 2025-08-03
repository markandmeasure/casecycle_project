from fastapi import Depends, FastAPI, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import uuid
from pathlib import Path
from jinja2 import Template
import time
import logging
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Histogram,
    CONTENT_TYPE_LATEST,
    generate_latest,
)

import models
from database import SessionLocal, engine
from settings import ALLOWED_ORIGINS

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Prometheus metrics registry and metrics definitions
PROMETHEUS_REGISTRY = CollectorRegistry()
REQUEST_COUNT = Counter(
    "requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
    registry=PROMETHEUS_REGISTRY,
)
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["method", "path"],
    registry=PROMETHEUS_REGISTRY,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request metrics and processing time."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    route = request.scope.get("route")
    path_template = getattr(route, "path", request.url.path)

    REQUEST_COUNT.labels(request.method, path_template, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.method, path_template).observe(process_time)

    logger.info(
        "%s %s completed in %.4f seconds",
        request.method,
        request.url.path,
        process_time,
    )
    return response


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(PROMETHEUS_REGISTRY),
        media_type=CONTENT_TYPE_LATEST,
    )


TEMPLATE_PATH = Path(__file__).with_name("prompt_templates.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger = logging.getLogger("uvicorn")
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
    user_id: int


class OpportunitySchema(OpportunityCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.name == username).first()
    if not user:
        return None
    return user


def create_access_token(data: dict) -> str:
    return uuid.uuid4().hex


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.token == token).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


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


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.name})
    user.token = access_token
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    market_description: Optional[str] = None
    tam_estimate: Optional[float] = Field(default=None, gt=0)
    growth_rate: Optional[float] = Field(default=None, ge=0)
    consumer_insight: Optional[str] = None
    hypothesis: Optional[str] = None


@app.post("/opportunities/", response_model=OpportunitySchema)
def create_opportunity(
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.id == opportunity.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_opportunity = models.Opportunity(**opportunity.model_dump())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


@app.get("/opportunities/", response_model=List[OpportunitySchema])
def read_opportunities(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Opportunity).offset(skip).limit(limit).all()


@app.get("/opportunities/{opportunity_id}", response_model=OpportunitySchema)
def read_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = (
        db.query(models.Opportunity)
        .filter(models.Opportunity.id == opportunity_id)
        .first()
    )
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity


@app.put("/opportunities/{opportunity_id}", response_model=OpportunitySchema)
@app.patch("/opportunities/{opportunity_id}", response_model=OpportunitySchema)
def update_opportunity(
    opportunity_id: int,
    opportunity: OpportunityUpdate,
    db: Session = Depends(get_db),
):
    db_opportunity = (
        db.query(models.Opportunity)
        .filter(models.Opportunity.id == opportunity_id)
        .first()
    )
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    update_data = opportunity.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_opportunity, key, value)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


@app.delete("/opportunities/{opportunity_id}", status_code=204)
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    db_opportunity = (
        db.query(models.Opportunity)
        .filter(models.Opportunity.id == opportunity_id)
        .first()
    )
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    db.delete(db_opportunity)
    db.commit()
    return Response(status_code=204)


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
