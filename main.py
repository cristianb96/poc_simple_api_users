import uvicorn
from fastapi import FastAPI

from app.api.routes import auth_router, users_router
from app.database.database import engine
from app.models.user import UserDB

UserDB.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Usuarios",
    description="API REST para gestión de usuarios",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
