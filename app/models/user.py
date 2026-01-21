from tortoise import fields, models


class User(models.Model):
    # pk=True: 기본키 설정
    # CharField는 generated=True(자동 생성)가 안 되므로 직접 ID를 부여해야 함
    user_id = fields.CharField(
        max_length=50, pk=True, description="사용자 고유 아이디 (문자열)"
    )

    # null=True: 값이 없어도 됨 (Optional)
    user_name = fields.CharField(
        max_length=100, null=True, description="사용자 이름/닉네임"
    )

    # 보안을 위해 비밀번호 원문이 아닌 해시값을 저장
    pwd_hash = fields.CharField(
        max_length=255, null=True, description="해싱된 비밀번호"
    )

    # 로그인 세션이나 리프레시 토큰 관리를 위한 필드
    token_id = fields.CharField(
        max_length=255, null=True, description="인증 토큰 식별자"
    )

    class Meta:
        table = "Users"  # 실제 데이터베이스에 생성될 테이블 이름

    def __str__(self):
        return f"User(id={self.user_id}, name={self.user_name})"
