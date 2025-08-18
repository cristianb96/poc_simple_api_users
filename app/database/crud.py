from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import UserCreate, UserDB, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserDB]:
    return db.query(UserDB).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate, hashed_password: str) -> UserDB:
    db_user = UserDB(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[UserDB]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field != "password":
            setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user_id: int, new_password: str) -> Optional[UserDB]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
