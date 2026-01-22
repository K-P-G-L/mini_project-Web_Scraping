from tortoise import fields, models


class TokenBlacklist(models.Model):
    """로그아웃된 토큰을 저장하는 테이블"""
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=255, unique=True)
    expires_at = fields.DatetimeField()
    blacklisted_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "token_blacklist"