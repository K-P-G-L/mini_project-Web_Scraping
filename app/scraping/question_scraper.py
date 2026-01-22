import requests
from bs4 import BeautifulSoup


class QuestionScraper:  # 질문 스크래핑 전용 클래스
    BASE_URL = "https://steemit.com/kr/@centering/507"

    def scrape(self) -> list[dict]:  # 메서드는 클래스보다 한 단계 들여쓰기
        # User-Agent 추가 (차단 방지 및 Mac 환경 명시)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(self.BASE_URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # ol 내부의 li 태그들을 모두 가져옵니다.
        cells = soup.select("div.MarkdownViewer ol li")

        results = []

        for cell in cells:
            content = cell.get_text(strip=True)
            # 텍스트가 존재하고, 최소 5자 이상인 것만 수집 (null 방지)
            if content and len(content) > 5:
                results.append(
                    {
                        "question_text": content  # 키 이름을 DB 모델과 동일하게!
                    }
                )

        return results
