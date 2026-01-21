from fastapi import APIRouter, HTTPException, status

from app.repositories.quote_repo import QuoteRepository # DB접근 Repository
from app.services.quote_service import QuoteService # 서비스 로직
from app.services.quote_scraping_service import QuoteScrapingService
from app.schemas.quote import QuoteResponse # API 응답 형태 (DTO)

router = APIRouter(prefix="/quotes", tags=["Quotes"]) # /quotes 엔드포인트로 묶음, Swagger에서 Quotes로 표시


@router.get("/random", response_model=QuoteResponse, status_code=status.HTTP_200_OK) #랜덤 명언 뽑기 라우터
async def get_random_quote(): # HTTP요청 비동기처리
    service = QuoteService(QuoteRepository()) # Repository를 Service에 주입!!! Router는 Service만 호출하게함

    try: # Service 호출하면 Service가 DTO반환
        return await service.get_random_quote() # Router는 그대로 return함
    except ValueError: # Service 예외 -> HTTP 예외
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="명언 없슈",
        )


@router.post("/scrape", status_code=status.HTTP_200_OK,
             )
async def scrape_quotes():
    repo = QuoteRepository()
    service = QuoteScrapingService(repo)

    count = await service.collect_and_save()
    return {"saved_count": count}
