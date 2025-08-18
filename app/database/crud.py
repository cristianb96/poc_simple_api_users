from datetime import datetime
from typing import Dict, List

from app.models.user import User, UserCreate, UserInDB, UserUpdate

users_db: Dict[int, UserInDB] = {}
user_id_counter = 1

def get_user_by_username(username: str) -> UserInDB | None:
    for user in users_db.values():
        if user.username == username:
            return user
    return None

def get_user_by_email(email: str) -> UserInDB | None:
    for user in users_db.values():
        if user.email == email:
            return user
    return None

def get_users() -> List[User]:
    return [User.from_orm(user) for user in users_db.values()]

def create_user(user: UserCreate, hashed_password: str) -> UserInDB:
    global user_id_counter
    user_id = user_id_counter
    user_id_counter += 1
    
    db_user = UserInDB(
        id=user_id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.now()
    )
    users_db[user_id] = db_user
    return db_user

def update_user(user_id: int, user_update: UserUpdate) -> UserInDB | None:
    if user_id not in users_db:
        return None
    
    db_user = users_db[user_id]
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field != "password":
            setattr(db_user, field, value)
    
    return db_user

def delete_user(user_id: int) -> bool:
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False
