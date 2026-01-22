import random

from app.models.question import Question


class QuestionRepository:
    """질문 데이터베이스 테이블에 접근하는 저장소 레이어"""

    async def get_random(self) -> Question | None:
        """모든 질문 중 하나를 무작위로 반환합니다."""
        all_questions = await Question.all()
        if not all_questions:
            return None
        return random.choice(all_questions)

    # 오류 때문에 null데이터 많이 쌓여있어서 추가한 로직..
    async def clear_all_questions(self):
        """
        기존 DB 클린하게함
        """
        await Question.all().delete()

    async def save_many(self, questions: list[dict]):
        """
        여러 개의 질문 데이터를 한 번에 저장합니다.
        """
        await Question.bulk_create(
            [
                Question(question_text=q.get("question_text") or q.get("content"))
                for q in questions
            ],
            ignore_conflicts=True,
        )
