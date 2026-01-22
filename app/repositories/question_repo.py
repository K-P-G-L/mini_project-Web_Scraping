import random

from tortoise import Tortoise
from tortoise.expressions import RawSQL

from app.models.question import Question


class QuestionRepository:
    """질문 데이터베이스 테이블에 접근하는 저장소 레이어"""

    async def get_random(self) -> Question | None:
        """
        [효율성 + 에러 방지]
        Raw SQL 대신 ORM 기능을 사용하여 랜덤하게 하나를 가져옵니다.
        PostgreSQL의 RANDOM() 함수를 안전하게 호출합니다.
        """
        try:
            # 1. annotate를 사용하여 무작위 값을 부여한 뒤 첫 번째 값을 가져옴
            return (
                await Question.all()
                .annotate(random_val=RawSQL("RANDOM()"))
                .order_by("random_val")
                .first()
            )
        except Exception as e:
            print(f"[Error] get_random 실패: {e}")
            # 대비책: 데이터가 적을 때는 전체에서 무작위 선택
            all_qs = await Question.all()
            return random.choice(all_qs) if all_qs else None

    async def clear_all_questions(self):
        """
        [번호 관리] 테이블을 비우고 ID를 1로 초기화합니다.
        """
        try:
            conn = Tortoise.get_connection("default")
            # Question 모델에 설정된 실제 테이블 이름을 가져옴
            table_name = Question._meta.db_table
            # PostgreSQL 전용 초기화 명령
            await conn.execute_script(
                f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;'
            )
        except Exception as e:
            print(f"[Error] clear_all_questions 실패: {e}")
            # TRUNCATE 실패 시 일반 삭제 수행
            await Question.all().delete()

    async def save_many(self, questions: list[dict]):
        """
        [데이터 정합성] 유효한 데이터만 필터링하여 일괄 저장합니다.
        """
        if not questions:
            return

        question_objs = []
        for q in questions:
            text = q.get("question_text") or q.get("content") or q.get("text")

            if text and isinstance(text, str) and text.strip():
                # 중복 방지를 위해 공백 제거 후 객체 생성
                question_objs.append(Question(question_text=text.strip()))

        if not question_objs:
            return

        await Question.bulk_create(
            question_objs,
            ignore_conflicts=True,
        )

    async def get_all(self) -> list[Question]:
        """모든 질문을 ID 순으로 반환합니다."""
        return await Question.all().order_by("id")
