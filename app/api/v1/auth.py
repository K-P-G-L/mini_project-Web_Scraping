import os
from datetime import datetime, timedelta

# FastAPI
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

# 암호화
from jose import jwt

from app.core.config import settings
from app.core.security import get_password_hash, new_token_id, verify_password

# 클래스 및 함수 불러오기
from app.models.user import User
from app.repositories.user_repo import get_user_by_username, logout_user

# OAuth2 토큰 추출 (스웨거 자물쇠 버튼 연동)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# JWT 설정값
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # 1) 토큰 디코드
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="아이디 또는 패스워드가 일치하지 않습니다.")

        # 2) 유저 조회
        user = await get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="로그인 실패")

        # 3) 토큰 만료 체크
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(status_code=401, detail="인증 토큰이 만료되었습니다.")

        # 4) 토큰 식별자(jti) 체크 (로그아웃 여부 확인)
        jti = payload.get("jti")
        if not jti or user.token_id != jti:
            raise HTTPException(status_code=401, detail="토큰값이 유효하지 않습니다.")

        return user

    except jwt.ExpireSignatureError:
        raise HTTPException(status_code=401, detail="인증 토큰이 만료되었습니다.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="토큰값이 유효하지 않습니다.")
    except Exception:
        raise HTTPException(status_code=401, detail="인증에 실패하셨습니다.")


# 회원가입 시 받을 데이터 정의
class RegisterBody(BaseModel):
    user_id: str
    user_name: str | None = None
    pwd_hash: str = Field(..., min_length=8)  # 비밀번호 8자 이상 강제


router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(payload: RegisterBody):
    # 아이디 중복 확인
    if await User.get_or_none(user_id=payload.user_id):
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")

    # 유저 생성 및 비밀번호 암호화 저장
    user = await User.create(
        user_id=payload.user_id,
        user_name=payload.user_name,
        pwd_hash=get_password_hash(payload.pwd_hash),
        token_id=None,
    )

    return {"user_id": user.user_id, "user_name": user.user_name}


@router.post("/login")
async def login(
    username: str = Form(...),  # 스웨거 Authorize 버튼은 'username'으로 데이터를 보냄
    password: str = Form(...),
):
    # DB에서 유저 찾기
    user = await User.get_or_none(user_id=username)

    if not user or not user.pwd_hash:
        raise HTTPException(status_code=400, detail="로그인 실패")

    # 비밀번호 검증
    if not verify_password(password, user.pwd_hash):
        raise HTTPException(status_code=400, detail="로그인 실패")

    # 새로운 토큰 ID 발급 (중복 로그인 방지 및 로그아웃 처리용)
    token_id = new_token_id()
    user.token_id = token_id
    await user.save(update_fields=["token_id"])

    # JWT 생성 (15분 만료)
    expire = datetime.utcnow() + timedelta(minutes=15)
    token = jwt.encode(
        {"sub": user.user_id, "jti": token_id, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    await logout_user(user.user_id)
    return {"message": "로그아웃 되었습니다."}