from datetime import datetime
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise

# 스키마 및 라우터 임포트
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate
from app.db.base import TORTOISE_CONFIG
from app.api.v1.quote import router as quote_router
from app.api.v1.question import router as question_router

app = FastAPI(title="FastAPI Mini Project - Unified")

# 라우터 등록: prefix를 /api/v1으로 설정
app.include_router(quote_router, prefix="/api/v1", tags=["Quotes"])
app.include_router(question_router, prefix="/api/v1", tags=["Questions"])

# 임시 DB (일기용)
fake_diary_db = []

def get_current_user() -> str:
    return "test_user"

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World! Database is connected."}

# --- 일기(Diary) CRUD API ---
@app.post("/diaries", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED, tags=["Diary"])
async def create_diary(diary_in: DiaryCreate, current_user: str = Depends(get_current_user)):
    new_diary = {
        "id": len(fake_diary_db) + 1,
        "title": diary_in.title,
        "content": diary_in.content,
        "author_id": current_user,
        "created_at": datetime.now()
    }
    fake_diary_db.append(new_diary)
    return new_diary

@app.get("/diaries", response_model=List[DiaryResponse], tags=["Diary"])
async def get_diaries():
    return fake_diary_db

# DB 연결 설정
# generate_schemas=True 로 설정하여 테이블이 없을 경우 자동으로 생성합니다.
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)
