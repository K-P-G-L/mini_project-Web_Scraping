import asyncio

from app.repositories.question_repo import QuestionRepository
from app.scraping.question_scraper import QuestionScraper


class QuestionScrapingService:
    """스크래핑 데이터를 수집하고 정리해서 DB에 저장함"""

    def __init__(self, repo: QuestionRepository):
        self.scraper = QuestionScraper()
        self.repo = repo

    async def collect_and_save(self) -> int:
        # 1. 동기 방식인 스크래퍼를 비동기 루프에서 안전하게 실행
        loop = asyncio.get_event_loop()
        questions = await loop.run_in_executor(None, self.scraper.scrape)

        if not questions:
            return 0

        # 2. 데이터 가공?: 'question_text' 또는 'content' 키에서 텍스트 추출 및 중복 제거
        unique_data = {}
        for q in questions:
            text = q.get("question_text") or q.get("content")
            if text and len(text.strip()) > 0:
                # 필드명을 'question_text'로 통일하여 딕셔너리 생성
                unique_data[text.strip()] = {"question_text": text.strip()}

        # 3. [중요] 기존 쓰레기 데이터 초기화
        # 새로운 데이터를 넣기 직전에 테이블을 비워 null 데이터가 뜨는걸 방지합니다 ㅠㅠ
        await self.repo.clear_all_questions()

        # 4. 정제된 데이터를 508개까지 저장 (블로그에 508개있음요)
        final_list = list(unique_data.values())[:508]
        await self.repo.save_many(final_list)

        return len(final_list)
