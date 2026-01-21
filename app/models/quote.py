from tortoise import fields
from tortoise.models import Model


class Quote(Model): # Quote(명언) 테이블
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.CharField(max_length=100, null=True)

    class Meta: #테이블 세부 설정
        table = "quotes" #데이터베이스 저장시 테이블이름 'quotes'
