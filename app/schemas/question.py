from pydantic import BaseModel


class QuestionResponse(BaseModel): # 자아성찰 API
    id: int
    content: str

    class Config:
        from_attributes = True # OMR객체 -> Schema변환 가능하게함
