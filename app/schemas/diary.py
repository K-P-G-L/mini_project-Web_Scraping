from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DiaryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {"title": "오늘의 일기", "content": "백엔드 개발은 정말 즐겁다."}
        }

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int  # 모델의 ForeignKey와 이름을 맞춤 (안전성 업!)
    created_at: datetime

    class Config:
        from_attributes = True