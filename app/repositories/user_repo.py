from app.models.user import User

async def get_user_by_username(username: str):
    return await User.get_or_none(user_name=username)