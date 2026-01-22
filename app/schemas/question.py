from pydantic import BaseModel, ConfigDict


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    # 문자열이거나, 없을 경우 None을 허용하도록 수정합니다.
    question_text: str | None = None
