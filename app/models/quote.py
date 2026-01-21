from tortoise import fields, models


class Quote(models.Model):
    quotes_id = fields.IntField(pk=True)
    content = fields.TextField(null=True)
    author = fields.CharField(max_length=100, null=True)

    class Meta:
        table = "Quotes"


class Bookmark(models.Model):
    bookmarks_id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="bookmarks")
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarked_by")

    class Meta:
        table = "Bookmarks"
        # 복합 유니크 제약 조건 (한 유저가 같은 명언 중복 북마크 방지)
        unique_together = (("user", "quote"),)
