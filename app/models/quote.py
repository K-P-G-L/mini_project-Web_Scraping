from tortoise import fields, models

# 1. 명언 원본 데이터를 저장하는 모델 (이게 빠져있어서 에러가 난 거야)
class Quote(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()   # 명언 내용
    author = fields.CharField(max_length=255, nullable=True) # 작가

    class Meta:
        table = "quotes"

# 2. 북마크 모델 (이름을 'Bookmark'로 통일할게)
class Bookmark(models.Model):
    id = fields.IntField(pk=True)
    # User와 Quote 모델을 연결
    user = fields.ForeignKeyField("models.User", related_name="bookmarks")
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarked_by")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "bookmarks"
        # 한 유저가 같은 명언을 중복해서 북마크하는 것 방지
        unique_together = (("user", "quote"),)