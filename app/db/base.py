import os
from pathlib import Path

from dotenv import load_dotenv

# 프로젝트 루트의 .env.dev 파일을 읽어옵니다.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.dev")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tortoise ORM 설정 딕셔너리
TORTOISE_CONFIG = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models",  # __init__.py를 통해 모든 모델을 한 번에 가져옴
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
