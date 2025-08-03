from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

import models
from database import SessionLocal, engine
from settings import ALLOWED_ORIGINS

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str


class UserSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class OpportunityCreate(BaseModel):
    title: str
    market_description: Optional[str] = None
    tam_estimate: Optional[float] = Field(default=None, gt=0)
    growth_rate: Optional[float] = Field(default=None, ge=0)
    consumer_insight: Optional[str] = None
    hypothesis: Optional[str] = None


class OpportunitySchema(OpportunityCreate):
    id: int

    class Config:
        orm_mode = True

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
    db_opportunity = models.Opportunity(**opportunity.dict())
    db.add(db_opportunity)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Title already exists")
    db.refresh(db_opportunity)
    return db_opportunity


@app.get("/opportunities/", response_model=List[OpportunitySchema])
def read_opportunities(db: Session = Depends(get_db)):
    return db.query(models.Opportunity).all()


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
