from typing import List, Optional, Tuple

from tortoise.exceptions import IntegrityError

from app.repositories.quote_repo import QuoteRepository
from app.schemas.quote import QuoteResponse


class QuoteService:
    def __init__(self, repo: QuoteRepository):
        self.repo = repo

    # 1. 랜덤 명언 제공 로직
    async def get_random_quote(self) -> Optional[QuoteResponse]:
        quote = await self.repo.get_random()
        if quote is None:
            return None
        return QuoteResponse.model_validate(quote)

    # 2. 북마크 추가 (중복 방지 및 상세 메시지)
    async def add_bookmark(self, user, quote_id: int) -> Tuple[bool, str]:
        # 명언 존재 여부 확인
        quote = await self.repo.get_by_id(quote_id)
        if not quote:
            return False, "존재하지 않는 명언입니다."

        try:
            await self.repo.create_bookmark(user=user, quote=quote)
            return True, "북마크에 성공적으로 추가되었습니다."
        except IntegrityError:
            # unique_together 제약 조건 위반 시
            return False, "이미 북마크에 등록된 명언입니다."

    # 3. 북마크 상세 조회
    async def get_user_bookmarks_detail(self, user) -> List[QuoteResponse]:
        quotes = await self.repo.get_bookmarks_by_user(user)
        # model_validate를 사용하여 ORM 객체를 Pydantic 모델로 변환
        return [QuoteResponse.model_validate(q) for q in quotes]

    # 4. 북마크 해제 (안내 문구 반환 필수 로직)
    async def remove_bookmark(self, user, quote_id: int) -> Tuple[bool, str]:
        """
        성공 시 (True, 삭제 메시지)
        실패 시 (False, 실패 사유 메시지) 반환
        """
        # Repository에서 삭제 수행 (성공 시 True 반환하도록 설계됨)
        success = await self.repo.delete_bookmark(user, quote_id)

        if success:
            # [수정] 안내 문구를 명확하게 전달
            return True, f"{quote_id}번 명언이 북마크에서 삭제되었습니다."
        else:
            # [수정] 존재하지 않거나 본인 것이 아닐 때의 피드백
            return False, "삭제할 북마크가 없거나 삭제 권한이 없습니다."
