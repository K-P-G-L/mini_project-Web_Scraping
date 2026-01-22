from typing import List
import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

# --- [추가] 3. CORS 설정 ---
# 프론트엔드(브라우저)에서 백엔드 API에 접근할 수 있도록 허용합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 단계에서는 모두 허용, 배포 시 특정 도메인으로 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. 라우터 등록 ---
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(quote_router, prefix="/api/v1", tags=["Quotes"])
app.include_router(question_router, prefix="/api/v1", tags=["Questions"])

# --- [추가] 5. 정적 파일 및 메인 페이지 설정 ---
# app/static 폴더가 없다면 생성해야 합니다.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# /static 경로로 정적 파일 제공
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")



# --- 6. Tortoise ORM 설정 ---
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

# --- 7. 비즈니스 로직 (Diary) ---

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
    # user_id가 모델 정의에 따라 다를 수 있으니 확인 필요 (현재 user_name 사용 중)
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


# [미션: 일기 삭제]
@app.delete(
    "/diaries/{diary_id}",
    status_code=status.HTTP_200_OK,
    tags=["Diary"],
)
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await Diary.get_or_none(id=diary_id, user_id=current_user.user_name)

    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일기를 찾을 수 없거나 삭제 권한이 없습니다.",
        )

    await diary.delete()

    return {
        "status": "success",
        "message": f"{diary_id}번 일기가 성공적으로 삭제되었습니다.",
    }

@app.get("/", tags=["Root"])
async def read_root():
    # 사용자가 접속했을 때 app/static/index.html 파일을 보여줍니다.
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Hello World! static/index.html 파일을 생성해주세요."}
