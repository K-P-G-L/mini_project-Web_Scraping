from tortoise import fields, models


class Question(models.Model):
    question_id = fields.IntField(pk=True)
    question_text = fields.TextField(null=True)

    class Meta:
        table = "Questions"


class UserQuestion(models.Model):
    user_question = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="user_questions")
    question = fields.ForeignKeyField("models.Question", related_name="answered_users")

    class Meta:
        table = "User_Questions"
