from tortoise import fields, models


class Diary(models.Model):
    id = fields.IntField(pk=True)
    # 1:N 관계 설정 (User와 연결)
    user = fields.ForeignKeyField("models.User", related_name="diaries")
    title = fields.CharField(max_length=255, null=True)
    content = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "Diaries"
