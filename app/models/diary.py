from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from tortoise import fields, models


# 1. 데이터베이스 모델 (Tortoise-ORM)
class Diary(models.Model):
    id = fields.IntField(pk=True)

    # 보안 및 성능: user_id에 index=True를 추가하여 검색 속도를 높였습니다.
    # qqqq... 와 같은 문자열 ID를 수용하도록 CharField 유지
    user_id = fields.CharField(max_length=100, index=True)

    title = fields.CharField(max_length=100)
    content = fields.TextField()

    # 생성 시각 자동 저장
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "diaries"

    def __str__(self):
        return f"{self.user_id}'s diary: {self.title}"


# 2. Pydantic 스키마 (데이터 검증 및 응답용)
class DiaryBase(BaseModel):
    # 유효성 검사: 제목은 최소 1자 이상, 100자 이하
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., description="일기 본문 내용")


class DiaryCreate(DiaryBase):
    """일기 생성 시 필요한 데이터"""

    pass


class DiaryUpdate(BaseModel):
    """일기 수정 시 선택적으로 데이터를 받을 수 있음"""

    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = None


class DiaryResponse(DiaryBase):
    """API 응답 시 클라이언트에게 전달할 데이터 구조"""

    id: int
    user_id: str
    created_at: datetime

    # Pydantic V2 설정 (Tortoise 객체를 JSON으로 변환 허용)
    model_config = ConfigDict(from_attributes=True)
