from app.models.question import ReflectionQuestion

class QuestionRepository: # 질문 테이블 접근 전용
    async def get_random(self) -> ReflectionQuestion | None: # 랜덤 질문 1개 가져오기
        return await ReflectionQuestion.all().order_by("?").first() #명언과 동일
