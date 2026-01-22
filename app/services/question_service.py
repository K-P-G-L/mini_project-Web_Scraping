# API용 비즈니스 로직
from app.repositories.question_repo import QuestionRepository
from app.schemas.question import QuestionResponse


class QuestionService:  # 명
    def __init__(self, repo: QuestionRepository):  # Repository를 외부에서 받음
        self.repo = repo

    async def get_random_question(
        self,
    ) -> (
        QuestionResponse
    ):  # 랜덤 질문 제공하는 로직 (반환 타입은 QuoteResponse(스키마))
        question = await self.repo.get_random()  # DB에서 랜덤 1줄 가져옴

        if question is None:  # 질문이 하나도 없을 때
            raise ValueError(
                "No question found"
            )  # HTTPException으로 바뀔 예정 (Repository에서는 X)

        return QuestionResponse.model_validate(question)  # ORM 모델 -> API응답 DTO 반환
