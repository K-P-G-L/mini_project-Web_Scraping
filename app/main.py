from fastapi import FastAPI, Depends, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from datetime import datetime
from typing import List, Optional

# 1. 경로 임포트 정리
try:
    from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate
except ImportError:
    from schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate

from app.db.base import TORTOISE_CONFIG

# [중요] 앱 선언은 한 번만 합니다!
app = FastAPI(title="FastAPI Mini Project")

# 2. DB 연결 설정 (app 선언 바로 아래에 위치)
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)

# 임시 DB
fake_diary_db = []

# 3. 인증 함수 (의존성 주입용)
def get_current_user() -> str:
    return "test_user"

@app.get("/")
async def read_root():
    return {"message": "Database is connected."}

# [CREATE] 일기 작성
@app.post("/diaries", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(
    diary_in: DiaryCreate,
    current_user: str = Depends(get_current_user)
):
    # Pydantic 모델 데이터를 딕셔너리로 변환
    new_diary = {
        "id": len(fake_diary_db) + 1,
        "title": diary_in.title,
        "content": diary_in.content,
        "author_id": current_user,
        "created_at": datetime.now()
    }
    fake_diary_db.append(new_diary)
    return new_diary

# [READ] 일기 목록 조회 (추가해두면 테스트하기 편합니다)
@app.get("/diaries", response_model=List[DiaryResponse])
async def get_diaries():
    return fake_diary_db

# [UPDATE] 일기 수정
@app.patch("/diaries/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    diary_in: DiaryUpdate,
    current_user: str = Depends(get_current_user)
):
    db_diary = next((d for d in fake_diary_db if d["id"] == diary_id), None)

    if not db_diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")
    if db_diary["author_id"] != current_user:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")

    # 수정 요청온 필드만 업데이트
    update_data = diary_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        db_diary[key] = value

    return db_diary

# [DELETE] 일기 삭제
@app.delete("/diaries/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(diary_id: int, current_user: str = Depends(get_current_user)):
    global fake_diary_db
    db_diary = next((d for d in fake_diary_db if d["id"] == diary_id), None)

    if not db_diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")
    if db_diary["author_id"] != current_user:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")

    fake_diary_db = [d for d in fake_diary_db if d["id"] != diary_id]
    return None