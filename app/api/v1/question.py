from fastapi import APIRouter, HTTPException, status

from app.repositories.question_repo import QuestionRepository # DB접근 Repository
from app.services.question_service import QuestionService # 서비스 로직
from app.schemas.question import QuestionResponse # API 응답 형태 (DTO)

router = APIRouter(prefix="/questions", tags=["Questions"]) # /questions 엔드포인트로 묶음, Swagger에서 Quotes로 표시


@router.get("/random", response_model=QuestionResponse, status_code=status.HTTP_200_OK) #랜덤 질문 뽑기 라우터
async def get_random_question(): # HTTP요청 비동기처리
    service = QuestionService(QuestionRepository()) # Repository를 Service에 주입!!! Router는 Service만 호출하게함

    try: # Service 호출하면 Service가 DTO반환
        return await service.get_random_question() # Router는 그대로 return함
    except ValueError: # Service 예외 -> HTTP 예외
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="질문이 없엉",
        )
