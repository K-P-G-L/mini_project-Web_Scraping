import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.repositories.user_repo import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="로그인 실패")

        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="로그인 실패")

        # (선택) 로그아웃/세션 무효화 지원: jti 확인
        jti = payload.get("jti")
        if user.token_id and jti and user.token_id != jti:
            raise HTTPException(status_code=401, detail="세션이 만료되었습니다.")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="인증 토큰이 만료되었습니다.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="토큰값이 유효하지 않습니다.")
    except Exception:
        raise HTTPException(status_code=401, detail="인증에 실패하셨습니다.")