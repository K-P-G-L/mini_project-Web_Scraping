from app.models.user import User


async def get_user_by_username(username: str):
    return await User.get_or_none(user_name=username)

async def logout_user(user_id: str):
    user = await User.get_or_none(user_id=user_id)
    if not user:
        return None
    
    user.token_id = None
    await user.save(update_fields=["token_id"])
    return user