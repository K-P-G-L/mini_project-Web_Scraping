import os
import uuid
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

# 비밀번호 암호화 컨텍스트
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# JWT 설정값
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def get_password_hash(password: str) -> str:
    # 평문 비밀번호를 해시로 변환
    return pwd_context.hash(password)

def verify_password(plain_password: str, pwd_hash: str) -> bool:
    # 입력된 비밀번호와 저장된 해시 비교
    return pwd_context.verify(plain_password, pwd_hash)

def new_token_id() -> str:
    return uuid.uuid4().hex

def create_access_token(subject: str, token_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "jti": token_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)