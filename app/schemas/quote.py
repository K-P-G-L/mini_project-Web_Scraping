from pydantic import BaseModel

class QuoteResponse(BaseModel): #명언 응답 전용 클래스
    id: int
    content: str
    author: str | None

    class Config:
        from_attributes = True #ORM 객체 -> Schema 변환 허용