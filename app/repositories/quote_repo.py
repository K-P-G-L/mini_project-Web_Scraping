from app.models.quote import Quote


class QuoteRepository: # 명언(Quote) 테이블에 접근하는 클래스 (명언 DB담당)
    async def get_random(self) -> Quote | None: # 랜덤 명언 1개 -> Quote 또는 None
        return await Quote.all().order_by("?").first() # quotes테이블 전체, DB 랜덤 정렬 후, 첫번째 1개


