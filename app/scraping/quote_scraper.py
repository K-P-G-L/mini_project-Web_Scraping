# HTML 수집만 담당합니다
import time

import requests
from bs4 import BeautifulSoup


class QuoteScraper:  # 명언 스크래핑 전용 클래스
    BASE_URL = "https://saramro.com/quotes"

                                # 수집 하는 페이지 수
    def scrape(self, max_pages: int = 10) -> list[dict]:  # 명언을 수집하는 메서드
        results = []  # 모든 페이지의 결과를 담을 리스트

        for page in range(1, max_pages + 1):
            # 1. 페이지별 URL 생성 (1페이지는 기본, 2페이지부터는 ?page=2 등)
            url = f"{self.BASE_URL}?page={page}"

            try:
                # 2. HTTP 요청 및 에러 체크
                response = requests.get(url, timeout=5)
                response.raise_for_status()

                # 3. HTML 파싱
                soup = BeautifulSoup(response.text, "html.parser")

                # 4. 명언 데이터가 담긴 셀 선택
                cells = soup.select('td[colspan="5"]')

                # 더 이상 긁을 데이터가 없으면 루프 종료
                if not cells:
                    break

                # 5. 각 셀에서 명언과 저자 추출
                for cell in cells:
                    text = cell.get_text(separator="\n", strip=True)
                    # 빈 줄을 제외하고 텍스트 라인 정리
                    lines = [line.strip() for line in text.split("\n") if line.strip()]

                    if lines:
                        content = lines[0]  # 첫 번째 줄은 명언 내용
                        # 줄이 여러 개면 마지막 줄을 저자로, 아니면 작자미상 처리
                        author = (
                            lines[-1].replace("-", "").strip()
                            if len(lines) > 1
                            else "작자미상"
                        )

                        results.append(
                            {
                                "content": content,
                                "author": author,
                            }
                        )

                # 6. 사이트 부하 방지를 위한 짧은 휴식 (에티켓)
                time.sleep(0.3)

            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                continue

        return results  # 누적된 모든 데이터 반환