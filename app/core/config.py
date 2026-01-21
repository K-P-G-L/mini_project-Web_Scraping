from pathlib import Path

from pydantic_settings import BaseSettings

# 프로젝트 루트 경로 찾기 (app 폴더의 상위 폴더)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        # Tortoise ORM용 URL 형식
        return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = {
        # 프로젝트 루트에 있는 .env.dev 파일을 읽도록 설정
        "env_file": BASE_DIR / ".env.dev",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # 다른 변수가 있어도 에러 방지
    }


# 이 한 줄이 있어야 'from app.core.config import settings'가 작동합니다.
settings = Settings()
