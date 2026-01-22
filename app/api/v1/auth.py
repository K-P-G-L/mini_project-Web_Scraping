import os
from datetime import datetime, timedelta

# FastAPI
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi import Form

# 암호화
from jose import jwt

# 클래스 및 함수 불러오기
from app.models.user import User
from app.repositories.user_repo import get_user_by_username
from app.core.security import verify_password, get_password_hash, new_token_id
from app.repositories.user_repo import logout_user

# OAuth2 토큰 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# JWT 설정값
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # 1) 토큰 디코드
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        # 유저가 존재하지 않을 경우 401 에러 발생
        if not username:
            raise HTTPException(status_code=401, detail="아이디 또는 패스워드가 일치하지 않습니다.")

        # 2) 유저 조회
        user = await get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="로그인 실패")

        # 3) 토큰 만료 체크
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}
        )
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(status_code=401, detail="인증 토큰이 만료되었습니다.")

        # 4) 토큰 식별자(jti) 체크
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


# 회원가입 및 로그인 엔드포인트
from pydantic import BaseModel

class RegisterBody(BaseModel):
    user_id: str
    user_name: str | None = None
    pwd_hash: str

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(payload: RegisterBody):
    if await User.get_or_none(user_id=payload.user_id):
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")
    
    user = await User.create(
        user_id=payload.user_id,
        user_name=payload.user_name,
        pwd_hash=get_password_hash(payload.pwd_hash),
        token_id=None
    )

    return {
        "user_id": user.user_id,
        "user_name": user.user_name
    }

@router.post("/login")
async def login(
    user_id: str = Form(...),
    password: str= Form(...)
):
    user = await User.get_or_none(user_id=user_id)
    if not user or not user.pwd_hash:
        raise HTTPException(status_code=400, detail="로그인 실패")
    
    if not verify_password(password, user.pwd_hash):
        raise HTTPException(status_code=400, detail="로그인 실패")
    
    # token_id = new_token_id()
    # user.token_id = token_id
    # await user.save(update_fields=["token_id"])

    # expire = datetime.utcnow() + timedelta(minutes=15)
    # token = jwt.encode(
    #     {"sub": user.user_id, "jti": token_id, "exp": expire},
    #     SECRET_KEY,
    #     algorithm=ALGORITHM
    # )

    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    user=Depends(get_current_user)):
    result = await logout_user(user.user_id)
    return {"message": "로그아웃 되었습니다."}

