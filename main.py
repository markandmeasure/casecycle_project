from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from pathlib import Path
from jinja2 import Template
from jose import JWTError, jwt
from passlib.context import CryptContext

import models
from database import SessionLocal, engine
from settings import ALLOWED_ORIGINS

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

TEMPLATE_PATH = Path(__file__).with_name("prompt_templates.json")

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    name: str
    password: str


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

@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/opportunities/", response_model=OpportunitySchema)
def create_opportunity(
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
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
    return (
        db.query(models.Opportunity)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/prompt/{opportunity_id}")
def generate_prompt(
    opportunity_id: int,
    template_name: str = "default",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
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
