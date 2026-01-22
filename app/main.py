from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, status
from tortoise.contrib.fastapi import register_tortoise

# 설정 및 라우터 임포트
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.question import router as question_router
from app.api.v1.quote import router as quote_router

# 스키마 임포트
from app.schemas.diary import DiaryCreate, DiaryResponse

app = FastAPI(title="FastAPI Locle Lab Project")

# --- 1. 라우터 등록 ---
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(quote_router, prefix="/api/v1", tags=["Quotes"])
app.include_router(question_router, prefix="/api/v1", tags=["Questions"])

# --- 2. Tortoise ORM 설정 (핵심 수정 사항) ---
# 모델 경로를 명확히 지정하여 'default_connection' 에러를 방지합니다.
MY_TORTOISE_CONFIG = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            # app.models.user 안에 User와 TokenBlacklist가 모두 있어야 합니다.
            "models": ["app.models.user", "aerich.models","app.models.auth","app.models.quote","app.models.question"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=MY_TORTOISE_CONFIG,
    generate_schemas=True,  # 새로운 테이블(TokenBlacklist) 생성을 위해 True 설정
    add_exception_handlers=True,
)

# --- 3. 기타 비즈니스 로직 (일기 등) ---
fake_diary_db = []

def get_current_user() -> str:
    return "test_user"

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World! Database is connected and Models are loaded."}

@app.post(
    "/diaries",
    response_model=DiaryResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Diary"],
)
async def create_diary(
    diary_in: DiaryCreate, current_user: str = Depends(get_current_user)
):
    new_diary = {
        "id": len(fake_diary_db) + 1,
        "title": diary_in.title,
        "content": diary_in.content,
        "author_id": current_user,
        "created_at": datetime.now(),
    }
    fake_diary_db.append(new_diary)
    return new_diary

@app.get("/diaries", response_model=List[DiaryResponse], tags=["Diary"])
async def get_diaries():
    return fake_diary_db