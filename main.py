from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
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


class UserSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class OpportunitySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


@app.post("/users/", response_model=UserSchema)
def create_user(name: str, db: Session = Depends(get_db)):
    user = models.User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get("/opportunities/", response_model=List[OpportunitySchema])
def read_opportunities(db: Session = Depends(get_db)):
    return db.query(models.Opportunity).all()
