from passlib.context import CryptContext
import uuid

# 비밀번호 암호화 컨텍스트
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    """평문 비밀번호를 해시로 변환"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력된 비밀번호와 저장된 해시 비교"""
    return pwd_context.verify(plain_password, hashed_password)

def new_token_id() -> str:
    return uuid.uuid4().hex