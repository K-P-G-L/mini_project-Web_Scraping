from app.models.quote import Quote
from tortoise.transactions import in_transaction


class QuoteRepository:  # 명언(Quote) 테이블에 접근하는 클래스 (명언 DB담당)
    async def get_random(self) -> Quote | None:  # 랜덤 명언 1개
        return await Quote.all().order_by("?").first()

    async def save_many(self, quotes: list[dict]) -> None: # 스크래핑 결과 여러개 저장용
        async with in_transaction(): #중간 실패 -> 전체 롤백 (하나의 트랜잭션으로 묶)
            for q in quotes:
                await Quote.get_or_create( #이미 있으면 가져오고 없으면 생성 (중복 방지)
                    content=q["content"], # key를 이용해 명언 본문 문자열
                    defaults={"author": q["author"]}, # '새롭게 생성시'
                )
