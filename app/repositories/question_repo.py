import random

from app.models.question import Question


class QuestionRepository:  # 질문 테이블 접근 전용
    async def get_random(self) -> Question | None:  # 랜덤 질문 1개 가져오기
        # PostgreSQL 필드 에러 방지를 위해 전체를 가져와서 랜덤 선택합니다.
        all_questions = await Question.all()

        if not all_questions:
            return None

        return random.choice(all_questions)
