import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./users.db")

settings = Settings()
