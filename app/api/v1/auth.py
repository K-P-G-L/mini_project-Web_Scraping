# FastAPI
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import get_current_user

# 참조 파일
from app.schemas.auth import RegisterRequest, TokenResponse
from app.services.auth_service import login_user, logout_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(payload: RegisterRequest):
    user = await register_user(payload.user_id, payload.user_name, payload.password)
    return {"user_id": user.user_id, "user_name": user.user_name}

@router.post("/login", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    token = await login_user(form.username, form.password)
    return TokenResponse(access_token=token)

@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    await logout_user(user)
    return {"message": "로그아웃 되었습니다."}