from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise

from app.api.v1.auth import get_current_user
from app.api.v1.auth import router as auth_router  # 실제 인증 함수 임포트
from app.api.v1.question import router as question_router
from app.api.v1.quote import router as quote_router

# 설정 및 라우터 임포트
from app.core.config import settings

# 모델 및 스키마 임포트
from app.models.diary import Diary
from app.models.user import User
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate

app = FastAPI(title="FastAPI Locle Lab Project")

# --- 1. 라우터 등록 ---
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(quote_router, prefix="/api/v1", tags=["Quotes"])
app.include_router(question_router, prefix="/api/v1", tags=["Questions"])

# --- 2. Tortoise ORM 설정 ---
MY_TORTOISE_CONFIG = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.auth",
                "app.models.quote",
                "app.models.question",
                "app.models.diary",  # 일기 모델 추가됨
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

# --- 3. 비즈니스 로직 (Root & Diary) ---


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
    # 실제 DB(Diary 모델)에 데이터 생성
    new_diary = await Diary.create(
        title=diary_in.title, content=diary_in.content, user=current_user
    )
    return new_diary


# [미션: 일기 전체 조회 (본인 것만)]
@app.get("/diaries", response_model=List[DiaryResponse], tags=["Diary"])
async def get_diaries(current_user: User = Depends(get_current_user)):
    # 보안: filter를 사용하여 로그인한 사용자의 일기만 반환
    return await Diary.filter(user=current_user).all()


# [미션: 일기 수정 (본인 확인 필수)]
@app.put("/diaries/{diary_id}", response_model=DiaryResponse, tags=["Diary"])
async def update_diary(
    diary_id: int, diary_in: DiaryUpdate, current_user: User = Depends(get_current_user)
):
    # prefetch_related로 연관된 유저 정보까지 한 번에 가져옴
    diary = await Diary.get_or_none(id=diary_id).prefetch_related("user")

    if not diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")

    # [권한 체크] 작성자와 현재 로그인 유저가 다른지 확인
    if diary.user.user_name != current_user.user_name:
        raise HTTPException(status_code=403, detail="자신의 일기만 수정할 수 있습니다.")

    # 전달된 값만 업데이트 (exclude_unset=True)
    update_data = diary_in.model_dump(exclude_unset=True)
    await diary.update_from_dict(update_data).save()
    return diary


# [미션: 일기 삭제 (본인 확인 필수)]
@app.delete(
    "/diaries/{diary_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Diary"]
)
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await Diary.get_or_none(id=diary_id).prefetch_related("user")

    if not diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")

    # [권한 체크]
    if diary.user.user_name != current_user.user_name:
        raise HTTPException(status_code=403, detail="자신의 일기만 삭제할 수 있습니다.")

    await diary.delete()
    return None
