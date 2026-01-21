import asyncio

from app.repositories.quote_repo import QuoteRepository
from app.scraping.quote_scraper import QuoteScraper


class QuoteScrapingService:
    def __init__(self, repo: QuoteRepository):
        self.scraper = QuoteScraper()
        self.repo = repo

    async def collect_and_save(self) -> int:
        # 1. 스크래핑 실행
        # (만약 scrape()가 비동기가 아니라면 별도 스레드에서 실행하여 서버 멈춤 방지)
        loop = asyncio.get_event_loop()
        quotes = await loop.run_in_executor(None, self.scraper.scrape)

        if not quotes:
            return 0

        # 2. 중복 제거 (내용 기준)
        unique = {q["content"]: q for q in quotes}

        # 3. DB 저장 (이미 작성하신 Repository의 save_many 호출)
        await self.repo.save_many(list(unique.values()))

        return len(unique)
