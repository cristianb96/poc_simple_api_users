from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserCreate(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
