from app.scraping.quote_scraper import QuoteScraper #명언 긁어오기 스크래퍼
from app.repositories.quote_repo import QuoteRepository # DB에 저장하는 Repository


class QuoteScrapingService: #스크래핑 결과를 "처리+저장"하는 서비스
    def __init__(self, repo: QuoteRepository): #Repository를 외부에서 주입
        self.scraper = QuoteScraper()
        self.repo = repo

    async def collect_and_save(self) -> int: #스크래핑 -> 중복제거 -> DB저장까지
        quotes = self.scraper.scrape() # app/services/quote_scraping_service.py의 return값

        unique = {} #중복 제거용 딕셔너리(가공)
        for q in quotes:
            unique[q["content"]] = q # 키 = 명언내용 (같은 내용이면 덮어써서 중복제거)

        await self.repo.save_many(list(unique.values())) #중복 제거된 명언들만 DB에 저장
        return len(unique) #처리한 명언 개수
