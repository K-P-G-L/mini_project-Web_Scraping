#API용 비즈니스 로직
from app.repositories.quote_repo import QuoteRepository #DB 접근 담당 Repository
from app.schemas.quote import QuoteResponse # API에 반환할 Schema 소환
from tortoise.exceptions import IntegrityError

class QuoteService: # 라우터가 호출할 클래스
    def __init__(self, repo: QuoteRepository = None): # Repository를 외부에서 받음
        self.repo = repo or QuoteRepository()

    async def get_random_quote(self) -> QuoteResponse: # 랜덤 명언 제공하는 로직 (반환 타입은 QuoteResponse(스키마))
        quote = await self.repo.get_random() # DB에서 가져온 랜덤 1줄

        if quote is None: # 명언이 하나도 없을 때
            raise ValueError("No quote found") # HTTPException으로 바뀔 예정 (Repository에서는 X)

        return QuoteResponse.model_validate(quote) # ORM 모델 -> API응답 DTO 반환

    async def add_bookmark(self, user_id: int, quote_id: int):
        try:
            return await self.repo.create_bookmark(user_id, quote_id)
        except IntegrityError:
            # 중복 추가 방지 로직: DB 제약 조건 덕분에 안전하게 방어됨
            return None

    async def list_bookmarks(self, user_id: int):
        return await self.repo.get_user_bookmarks(user_id)

    async def remove_bookmark(self, user_id: int, quote_id: int):
        return await self.repo.delete_bookmark(user_id, quote_id)
