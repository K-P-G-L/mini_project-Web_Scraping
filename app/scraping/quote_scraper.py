#HTML 수집만 담당합니다요
import requests
from bs4 import BeautifulSoup


class QuoteScraper: #명언 스크래핑 전용 클래스 (명언을 긁어오기만 하는놈)
    BASE_URL = "https://saramro.com/quotes"

    def scrape(self) -> list[dict]: #명언을 수집하는 메서드
        response = requests.get(self.BASE_URL, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser") #HTML 문자열 파싱해서 soup객체로 변환
        cells = soup.select('td[colspan="5"]') # .quote-box 요소들 전부 선택

        results = [] #최종 결과를 담을 리스트

        for cell in cells: # 명령 하나씩 순회 for문
            text = cell.get_text(separator="\n", strip=True) #<br>기준 텍스트 추출 + 공백 제거
            lines = text.split("\n") # 줄 단위 분리

            content = lines[0] # 첫줄 = 명언 내용
            author = lines[-1].replace("-", "").strip() # 마지막줄 = 저자 / 문자 제거 + 공백 제거

            results.append(  #명언 1개를 dict로 만들어 리스트에 추가 ㅇㅇ
                {
                    "content": content,
                    "author": author,
                }
            )  # -> 여기서 만들어지는게 quotes = [{"content": "명언1", "author": "저자1"},{"content": "명언2", "author": "저자2"}]

        return results
