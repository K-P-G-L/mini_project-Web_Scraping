from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.question_repo import QuestionRepository
from app.schemas.question import QuestionResponse
from app.services.question_scraping_service import QuestionScrapingService
from app.services.question_service import QuestionService

router = APIRouter(prefix="/questions", tags=["Questions"])


# 의존성 주입
def get_question_service():
    return QuestionService(QuestionRepository())


def get_scraping_service():
    return QuestionScrapingService(QuestionRepository())


@router.get("/random", response_model=QuestionResponse, status_code=status.HTTP_200_OK)
async def get_random_question(
    service: QuestionService = Depends(get_question_service),
):
    question_dto = await service.get_random_question()
    if not question_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="저장된 질문이 없습니다. 스크래핑을 먼저 실행하세요.",
        )
    return question_dto


@router.post("/scrape", status_code=status.HTTP_200_OK)
async def scrape_questions(
    service: QuestionScrapingService = Depends(get_scraping_service),
):
    count = await service.collect_and_save()
    return {"message": "스크래핑 완료", "saved_count": count}
