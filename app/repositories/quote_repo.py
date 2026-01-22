import random
from typing import Dict, List, Optional

from tortoise.transactions import in_transaction

from app.models.quote import Bookmark, Quote  # Bookmark 모델 추가 소환!


class QuoteRepository:
    # --- 기존 메서드들 ---
    async def get_random(self) -> Optional[Quote]:
        all_quotes = await Quote.all()
        if not all_quotes:
            return None
        return random.choice(all_quotes)

    async def save_many(self, quotes: List[Dict[str, str]]) -> None:
        async with in_transaction():
            for q in quotes:
                await Quote.get_or_create(
                    content=q.get("content"),
                    defaults={"author": q.get("author", "Unknown")},
                )

    async def get_by_id(self, quote_id: int) -> Optional[Quote]:
        return await Quote.filter(quotes_id=quote_id).first()

    # --- 신규 추가: 북마크 관련 메서드 ---

    async def create_bookmark(self, user, quote: Quote) -> Bookmark:
        """북마크를 DB에 생성합니다. (unique_together에 의해 중복 시 에러 발생)"""
        return await Bookmark.create(user=user, quote=quote)

    async def get_bookmarks_by_user(self, user) -> List[Quote]:
        """
        사용자가 북마크한 명언 리스트를 가져옵니다.
        N+1 문제를 방지하기 위해 prefetch_related를 사용합니다.
        """
        # Bookmark 테이블을 조회하면서 연결된 Quote(명언) 정보를 미리 가져옵니다.
        bookmarks = await Bookmark.filter(user=user).prefetch_related("quote")
        # 결과에서 명언 객체들만 리스트로 추출합니다.
        return [b.quote for b in bookmarks]

    async def delete_bookmark(self, user, quote_id: int) -> bool:
        """특정 사용자의 특정 명언 북마크를 삭제합니다."""
        bookmark = await Bookmark.filter(user=user, quote_id=quote_id).first()
        if bookmark:
            await bookmark.delete()
            return True
        return False
