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


# 일기 수정 시 받을 데이터 (선택적)
class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# API 응답으로 내보낼 데이터 (DB의 id, 작성시간 등 포함)
class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: str
    created_at: datetime

    class Config:
        from_attributes = True  # ORM 모델을 자동으로 Pydantic으로 변환
