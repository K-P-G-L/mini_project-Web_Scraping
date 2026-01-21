from typing import Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50)
    user_name: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"