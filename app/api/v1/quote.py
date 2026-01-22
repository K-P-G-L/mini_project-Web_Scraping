from fastapi import APIRouter, HTTPException, status, Depends
from app.repositories.quote_repo import QuoteRepository
from app.services.quote_service import QuoteService
from app.services.quote_scraping_service import QuoteScrapingService
from app.schemas.quote import QuoteResponse

router = APIRouter(prefix="/quotes", tags=["Quotes"])

# 의존성 주입 도우미
def get_quote_service():
    return QuoteService(QuoteRepository())

def get_scraping_service():
    return QuoteScrapingService(QuoteRepository())

@router.get("/random", response_model=QuoteResponse, status_code=status.HTTP_200_OK)
async def get_random_quote(service: QuoteService = Depends(get_quote_service)):
    quote_dto = await service.get_random_quote()
    if not quote_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="저장된 명언이 없습니다. 스크래핑을 먼저 실행하세요."
        )
    return quote_dto

@router.post("/scrape", status_code=status.HTTP_200_OK)
async def scrape_quotes(service: QuoteScrapingService = Depends(get_scraping_service)):
    count = await service.collect_and_save()
    return {"message": "스크래핑 완료", "saved_count": count}
