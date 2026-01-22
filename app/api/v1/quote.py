from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.repositories.quote_repo import QuoteRepository
from app.services.quote_service import QuoteService
from app.services.quote_scraping_service import QuoteScrapingService
from app.schemas.quote import QuoteResponse, BookmarkRead


async def get_current_user():
    """인증 기능이 완성되기 전까지 사용하는 가짜 유저 함수"""
    return 1  # 일단 유저 ID를 1이라고 가정


# 1. 라우터 설정 (prefix는 main.py에서 중복되지 않게 확인)
router = APIRouter(prefix="/quotes", tags=["Quotes"])


# 2. 의존성 주입 도우미
def get_quote_service():
    return QuoteService()


def get_scraping_service():
    return QuoteScrapingService(QuoteRepository())


# --- 기존 기능 ---
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


# --- 북마크 기능 ---

@router.post("/bookmarks/{quote_id}", status_code=status.HTTP_201_CREATED)
async def add_bookmark(
        quote_id: int,
        current_user=Depends(get_current_user),
        service: QuoteService = Depends(get_quote_service)
):
    result = await service.add_bookmark(current_user, quote_id)
    # Service에서 중복 시 "already_exists"를 반환하도록 설계했다면 아래처럼 처리
    if result == "already_exists":
        raise HTTPException(status_code=400, detail="이미 북마크된 명언입니다.")
    if not result:
        raise HTTPException(status_code=404, detail="명언을 찾을 수 없습니다.")
    return {"status": "success", "bookmark_id": result.id}


@router.get("/bookmarks", response_model=List[BookmarkRead])
async def get_bookmarks(
        current_user=Depends(get_current_user),
        service: QuoteService = Depends(get_quote_service)
):
    # [핵심 수정] 에러가 났던 get_my_bookmarks 대신 repo를 활용해 데이터를 가져오고
    # 명언 정보(content, author)를 합쳐서 응답합니다.
    bookmarks = await service.repo.get_user_bookmarks(current_user)

    results = []
    for b in bookmarks:
        quote = await service.repo.get_by_id(b.quote_id)
        results.append({
            "id": b.id,
            "quote_id": b.quote_id,
            "content": quote.content if quote else "명언 정보 없음",
            "author": quote.author if quote else "Unknown",
            "created_at": b.created_at
        })
    return results


@router.delete("/bookmarks/{quote_id}")
async def delete_bookmark(
        quote_id: int,
        current_user=Depends(get_current_user),
        service: QuoteService = Depends(get_quote_service)
):
    # 서비스의 메서드 이름이 cancel_bookmark인지 확인 필요!
    success = await service.cancel_bookmark(current_user, quote_id)
    if not success:
        raise HTTPException(status_code=404, detail="북마크를 찾을 수 없습니다.")
    return {"status": "deleted"}