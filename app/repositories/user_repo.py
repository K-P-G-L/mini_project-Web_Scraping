from app.models.user import User


async def get_user_by_id(user_id: str):
    return await User.get_or_none(user_id=user_id)

async def get_user_by_username(user_name: str):
    return await User.get_or_none(user_name=user_name)


async def create_user(user_id: str, user_name: str | None, pwd_hash: str):
    return await User.create(
        user_id=user_id,
        user_name=user_name,
        pwd_hash=pwd_hash,
        token_id=None,
    )


async def update_token_id(user: User, token_id: str | None):
    user.token_id = token_id
    await user.save(update_fields=["token_id"])
    return user