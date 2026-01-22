import os
from datetime import datetime

# FastAPI
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# 암호화
from jose import jwt

# User 클래스 불러오기
from app.repositories.user_repo import get_user_by_username

# OAuth2 토큰 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
            raise HTTPException(status_code=401, detail="로그인 실패")

        # 2) 유저 조회
        user = await get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="로그인 실패")


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

        return user

    except jwt.ExpireSignatureError:
        raise HTTPException(status_code=401, detail="인증 토큰이 만료되었습니다.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="토큰값이 유효하지 않습니다.")
    except Exception:
        raise HTTPException(status_code=401, detail="인증에 실패하셨습니다.")
