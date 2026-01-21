from tortoise import fields, models

class TokenBlacklist(models.Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=500, index=True)  # 무효화된 토큰 값
    blacklisted_at = fields.DatetimeField(auto_now_add=True)  # 블랙리스트 등록 시간
    expires_at = fields.DatetimeField()  # 토큰의 원래 만료 시간 (이 시간이 지나면 DB에서 삭제 가능)

    class Meta:
        table = "token_blacklist"