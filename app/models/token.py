from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    username: Optional[str] = None
