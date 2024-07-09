from pydantic import BaseModel
from typing import List, Optional
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    project_id = Column(Integer)
    mobile_number = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    hashtag = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    password = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# Pydantic models
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    project_id: int

class UserCreate(UserBase):
    mobile_number: Optional[str] = None
    dob: Optional[str] = None
    hashtag: Optional[str] = None
    company_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    project_id: Optional[int] = None
    mobile_number: Optional[str] = None
    dob: Optional[str] = None
    hashtag: Optional[str] = None
    company_name: Optional[str] = None
    password: Optional[str] = None


