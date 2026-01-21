# FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# 암호화
from jose import jwt
from passlib.context import CryptContext

# db
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# JWT 설정값
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# 비밀번호 암호화 컨텍스트
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# OAuth2 토큰 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        result = await db.execute(
            select(User).filter(User.user_name == username)
        )
        user = result.scalars().first()

        # 유저가 존재하지 않을 경우 401 에러 발생
        if not username:
            raise HTTPException(status_code=401, detail="로그인 실패")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
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























