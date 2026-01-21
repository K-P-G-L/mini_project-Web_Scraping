from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    get_password_hash,
    new_token_id,
    verify_password,
)
from app.repositories.user_repo import (
    create_user,
    get_user_by_id,
    update_token_id,
)


async def register_user(user_id: str, user_name: str | None, password: str):
    existing = await get_user_by_id(user_id)
    if existing:
        raise HTTPException(status_code=409, detail="이미 존재하는 사용자 아이디입니다.")

    pwd_hash = get_password_hash(password)
    user = await create_user(user_id=user_id, user_name=user_name, pwd_hash=pwd_hash)
    return user

async def login_user(user_id: str, password: str) -> str:
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")

    if not user.pwd_hash or not verify_password(password, user.pwd_hash):
        raise HTTPException(status_code=401, detail="로그인 실패")

    tid = new_token_id()
    await update_token_id(user, tid)

    # create_access_token 시그니처에 맞게 subject에 user_id를 넣는다
    return create_access_token(subject=user.user_id, token_id=tid)

async def logout_user(user):
    # 토큰을 무효화: token_id 제거(또는 새 값으로 갱신)
    await update_token_id(user, None)
