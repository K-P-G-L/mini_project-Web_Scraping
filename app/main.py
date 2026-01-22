from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise

# 1. 의존성 및 라우터 임포트
from app.api.v1.auth import get_current_user
from app.api.v1.auth import router as auth_router
from app.api.v1.question import router as question_router
from app.api.v1.quote import router as quote_router

# 설정 임포트
from app.core.config import settings

# 모델 및 스키마 임포트
from app.models.diary import Diary
from app.models.user import User
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate

# 2. FastAPI 인스턴스 초기화
app = FastAPI(title="FastAPI Locle Lab Project")

# --- 3. 라우터 등록 ---
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(quote_router, prefix="/api/v1", tags=["Quotes"])
app.include_router(question_router, prefix="/api/v1", tags=["Questions"])

# --- 4. Tortoise ORM 설정 ---
MY_TORTOISE_CONFIG = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.auth",
                "app.models.quote",
                "app.models.question",
                "app.models.diary",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=MY_TORTOISE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)

# --- 5. 비즈니스 로직 (Root & Diary) ---


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World! Database is connected and Models are loaded."}


# [미션: 일기 작성]
@app.post(
    "/diaries",
    response_model=DiaryResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Diary"],
)
async def create_diary(
    diary_in: DiaryCreate, current_user: User = Depends(get_current_user)
):
    new_diary = await Diary.create(
        title=diary_in.title, content=diary_in.content, user_id=current_user.user_name
    )
    return new_diary


# [미션: 일기 전체 조회 (본인 것만)]
@app.get("/diaries", response_model=List[DiaryResponse], tags=["Diary"])
async def get_diaries(current_user: User = Depends(get_current_user)):
    return await Diary.filter(user_id=current_user.user_name).all()


# [미션: 일기 수정 (본인 확인 필수)]
@app.put("/diaries/{diary_id}", response_model=DiaryResponse, tags=["Diary"])
async def update_diary(
    diary_id: int, diary_in: DiaryUpdate, current_user: User = Depends(get_current_user)
):
    diary = await Diary.get_or_none(id=diary_id, user_id=current_user.user_name)

    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일기를 찾을 수 없거나 수정 권한이 없습니다.",
        )

    update_data = diary_in.model_dump(exclude_unset=True)
    await diary.update_from_dict(update_data).save()
    return diary


# [미션: 일기 삭제 (안내 문구 출력을 위해 200 OK로 수정)]
@app.delete(
    "/diaries/{diary_id}",
    status_code=status.HTTP_200_OK,  # <--- 204에서 200으로 변경!
    tags=["Diary"],
)
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    # 보안: 삭제 권한 확인
    diary = await Diary.get_or_none(id=diary_id, user_id=current_user.user_name)

    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일기를 찾을 수 없거나 삭제 권한이 없습니다.",
        )

    await diary.delete()

    # 204일 때는 무시되었던 이 반환값이 이제 200 응답 본문으로 전달됩니다.
    return {
        "status": "success",
        "message": f"{diary_id}번 일기가 성공적으로 삭제되었습니다.",
    }
