import random
from typing import Dict, List, Optional

from tortoise.transactions import in_transaction

from app.models.quote import Quote


class QuoteRepository:  # 명언(Quote) 테이블에 접근하는 클래스 (명언 DB담당)
    async def get_random(self) -> Optional[Quote]:
        """
        PostgreSQL의 order_by('?') 미지원 문제를 해결하기 위해
        모든 레코드를 조회 후 Python random 모듈로 1개를 선택합니다.
        """
        all_quotes = await Quote.all()
        if not all_quotes:
            return None
        return random.choice(all_quotes)

    async def save_many(self, quotes: List[Dict[str, str]]) -> None:
        """
        스크래핑 결과를 DB에 저장합니다.
        중복 방지를 위해 get_or_create를 사용하며, 트랜잭션으로 안전성을 보장합니다.
        """
        async with in_transaction():
            for q in quotes:
                # content가 동일한 명언이 이미 있다면 생성하지 않고 건너뜁니다.
                await Quote.get_or_create(
                    content=q.get("content"),
                    defaults={"author": q.get("author", "Unknown")},
                )

    async def get_by_id(self, quote_id: int) -> Optional[Quote]:
        """
        ID를 통해 특정 명언을 조회합니다. (상세 조회용)
        """
        return await Quote.filter(quotes_id=quote_id).first()
