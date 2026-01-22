import random
from typing import Dict, List, Optional

from tortoise.transactions import in_transaction

from app.models.quote import Quote, Bookmark

class QuoteRepository:
    # --- [명언 관리 기능] ---
    async def get_random(self) -> Optional[Quote]:
        """모든 명언 중 랜덤으로 1개 반환"""
        all_quotes = await Quote.all()
        if not all_quotes:
            return None
        return random.choice(all_quotes)

    async def save_many(self, quotes: List[Dict[str, str]]) -> None:
        """스크래핑 결과 저장 (중복 방지)"""
        async with in_transaction():
            for q in quotes:
                await Quote.get_or_create(
                    content=q.get("content"),
                    defaults={"author": q.get("author", "Unknown")},
                )

    async def get_by_id(self, quote_id: int) -> Optional[Quote]:
        """ID로 특정 명언 조회"""
        return await Quote.filter(id=quote_id).first()

    # --- [북마크 관리 기능] ---
    async def create_bookmark(self, user_id: int, quote_id: int):
        """
        [수정됨]
        user=user_id 대신 user_id=user_id를 사용하여
        객체가 아닌 숫자 ID 값을 직접 DB에 저장합니다.
        """
        return await Bookmark.create(
            user_id=user_id,
            quote_id=quote_id
        )

    async def get_user_bookmarks(self, user_id: int):
        """특정 유저의 북마크 목록 조회 (user_id로 필터링)"""
        return await Bookmark.filter(user_id=user_id).all()

    async def delete_bookmark(self, user_id: int, quote_id: int):
        """북마크 삭제 (user_id 필드 사용)"""
        return await Bookmark.filter(user_id=user_id, quote_id=quote_id).delete()