from tortoise import fields
from tortoise.models import Model


class ReflectionQuestion(Model): #성찰 질문(ReflectionQuestion)
    id = fields.IntField(pk=True)
    content = fields.TextField()

    class Meta:
        table = "reflection_questions" #데이터베이스 내에서의 실제 테이블 이름
