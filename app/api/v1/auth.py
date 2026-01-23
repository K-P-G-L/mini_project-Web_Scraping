import re
from datetime import datetime, timedelta, timezone

# 암호화 (명시적 임포트로 밑줄 방지)
import jose.jwt as jwt

# FastAPI
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, field_validator

from app.core.config import settings
from app.core.security import get_password_hash, new_token_id, verify_password
from app.models.auth import TokenBlacklist

# 모델 및 리포지토리 (정의된 모델만 호출하여 중복 제거)
from app.models.user import User
from app.repositories.user_repo import get_user_by_username, logout_user

# 1. OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# JWT 설정값
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# --- 의존성 주입 (인증 확인) ---


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # 1) 토큰 디코드
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        username = payload.get("sub")

        if not username or not jti:
            raise HTTPException(status_code=401, detail="인증 정보가 부정확합니다.")

        # 2) 블랙리스트 검사 (이미 로그아웃된 토큰인지 확인)
        if await TokenBlacklist.filter(token=jti).exists():
            raise HTTPException(status_code=401, detail="이미 로그아웃된 토큰입니다.")

        # 3) 유저 조회
        user = await get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="유저를 찾을 수 없습니다.")

        # 4) 이중 체크: 유저 테이블의 최신 토큰 ID와 일치하는지 확인
        if user.token_id != jti:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="인증 토큰이 만료되었습니다.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="토큰값이 유효하지 않습니다.")
    except Exception as e:
        # 에러 발생 시 Swagger Response Body에서 원인을 바로 확인할 수 있도록 수정
        raise HTTPException(status_code=401, detail=f"인증 실패 원인: {str(e)}")


# --- API 엔드포인트 ---

router = APIRouter(prefix="/auth")


class RegisterBody(BaseModel):
    user_id: str = Field(..., min_length=4)
    user_name: str | None = None
    pwd_hash: str = Field(..., min_length=8)

    @field_validator("pwd_hash")
    @classmethod  # V2에서는 classmethod를 붙여주는 것이 정석입니다.
    def validate_password_details(cls, v: str):
        if len(v) < 8:
            raise ValueError("비밀번호를 8글자 이상으로 만드시오.")

        # 영문(대소문자 무관) 체크
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("영문을 포함해주세요.")

        if not re.search(r"\d", v):
            raise ValueError("숫자를 포함해주세요.")

        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("특수문자를 포함해주세요.")

        return v


@router.post("/register")
async def register(payload: RegisterBody):
    if await User.get_or_none(user_id=payload.user_id):
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")

    user = await User.create(
        user_id=payload.user_id,
        user_name=payload.user_name,
        pwd_hash=get_password_hash(payload.pwd_hash),
        token_id=None,
    )
    return {"user_id": user.user_id, "user_name": user.user_name}


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await User.get_or_none(user_id=username)
    if not user or not user.pwd_hash or not verify_password(password, user.pwd_hash):
        raise HTTPException(status_code=400, detail="로그인 실패")

    token_id = new_token_id()
    user.token_id = token_id
    await user.save(update_fields=["token_id"])

    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    token = jwt.encode(
        {"sub": user.user_id, "jti": token_id, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), user=Depends(get_current_user)):
    payload = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
    )
    jti = payload.get("jti")
    exp = payload.get("exp")

    if jti and exp:
        try:
            # get_or_create로 중복 저장 에러 방지
            await TokenBlacklist.get_or_create(
                token=jti,
                defaults={"expires_at": datetime.fromtimestamp(exp, tz=timezone.utc)},
            )
        except Exception:
            pass

    await logout_user(user.user_id)
    return {"message": "로그아웃 되었습니다."}