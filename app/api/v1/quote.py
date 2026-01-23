from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

# 인증을 위한 get_current_user 임포트 (경로는 프로젝트에 맞게 확인해주세요)
from app.api.v1.auth import get_current_user
from app.repositories.quote_repo import QuoteRepository
from app.schemas.quote import QuoteResponse
from app.services.quote_scraping_service import QuoteScrapingService
from app.services.quote_service import QuoteService

router = APIRouter(prefix="/quotes", tags=["Quotes"])


# 의존성 주입 도우미
def get_quote_service():
    return QuoteService(QuoteRepository())


def get_scraping_service():
    return QuoteScrapingService(QuoteRepository())


# --- 기존 기능 ---


@router.get("/random", response_model=QuoteResponse, status_code=status.HTTP_200_OK)
async def get_random_quote(service: QuoteService = Depends(get_quote_service)):
    quote_dto = await service.get_random_quote()
    if not quote_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="저장된 명언이 없습니다. 스크래핑을 먼저 실행하세요.",
        )
    return quote_dto


@router.post("/scrape", status_code=status.HTTP_200_OK)
async def scrape_quotes(service: QuoteScrapingService = Depends(get_scraping_service)):
    count = await service.collect_and_save()
    return {"message": "스크래핑 완료", "saved_count": count}


# --- 신규 추가: 북마크 미션 기능 ---


@router.get("/bookmarks", response_model=List[QuoteResponse])
async def get_bookmarks(
    current_user=Depends(get_current_user),
    service: QuoteService = Depends(get_quote_service),
):
    """나의 모든 북마크 조회"""
    return await service.get_user_bookmarks_detail(current_user)


@router.post("/bookmarks/{quote_id}", status_code=status.HTTP_201_CREATED)
async def add_bookmark(
    quote_id: int,
    current_user=Depends(get_current_user),
    service: QuoteService = Depends(get_quote_service),
):
    """명언 북마크 추가 (중복 방지 로직 포함)"""
    success, message = await service.add_bookmark(current_user, quote_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return {"message": message}


@router.delete("/bookmarks/{quote_id}", status_code=status.HTTP_200_OK)
async def remove_bookmark(
    quote_id: int,
    current_user=Depends(get_current_user),
    service: QuoteService = Depends(get_quote_service),
):
    """북마크 해제"""
    success = await service.remove_bookmark(current_user, quote_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="북마크를 찾을 수 없습니다."
        )
    return {"message": "북마크가 해제되었습니다."}
