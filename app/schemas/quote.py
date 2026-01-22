from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class QuoteResponse(BaseModel):
    id: int
    content: str
    author: Optional[str] = "Unknown"

    model_config = ConfigDict(from_attributes=True)

class QuoteCreate(BaseModel):
    content: str
    author: str

class BookmarkCreate(BaseModel):
    quote_id: int
    content: Optional[str] = None
    author: Optional[str] = None

class BookmarkRead(BaseModel):
    id: int
    quote_id: int
    # [수정] Bookmark 테이블에 직접적인 content가 없을 확률이 높으므로
    # 기본값을 주어 500 에러를 방지합니다.
    content: Optional[str] = "명언 정보를 불러오는 중..."
    author: Optional[str] = "Unknown"
    created_at: datetime

    # Tortoise 모델을 Pydantic으로 자동 변환
    model_config = ConfigDict(from_attributes=True)