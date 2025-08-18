from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_active_user
from app.database.crud import (
    create_user,
    delete_user,
    get_password_hash,
    get_user_by_email,
    get_user_by_username,
    get_users,
    update_user,
    update_user_password,
)
from app.database.database import get_db
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["usuarios"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = create_user(db, user, hashed_password)
    return User.model_validate(db_user)

@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    users = get_users(db, skip=skip, limit=limit)
    return [User.model_validate(user) for user in users]

@router.put("/{user_id}", response_model=User)
async def update_user_info(
    user_id: int, 
    user_update: UserUpdate, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar este usuario"
        )
    
    db_user = update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_update.password:
        db_user = update_user_password(db, user_id, user_update.password)
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return User.model_validate(db_user)

@router.delete("/{user_id}")
async def delete_user_info(
    user_id: int, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este usuario"
        )
    
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"message": "Usuario eliminado exitosamente"}
