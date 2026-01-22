from pydantic import BaseModel, ConfigDict, Field


class QuoteResponse(BaseModel):
    # DB의 quotes_id를 API 응답에서는 id로 보여주도록 매핑
    id: int = Field(validation_alias="quotes_id")
    content: str
    author: str

    # Tortoise ORM 객체를 Pydantic 모델로 변환 허용 (매우 중요)
    model_config = ConfigDict(from_attributes=True)


class QuoteCreate(BaseModel):
    content: str
    author: str
