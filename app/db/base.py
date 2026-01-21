import os
from pathlib import Path

from dotenv import load_dotenv

# 현재 파일(base.py) 기준으로 프로젝트 루트(.env.dev가 있는 곳) 찾기
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.dev")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 변수들이 잘 로드되었는지 확인하기 위한 URL 조합
DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TORTOISE_CONFIG = {
    "connections": {
        "default": DATABASE_URL  # settings.DATABASE_URL 대신 직접 만든 DATABASE_URL 사용
    },
    "apps": {
        "models": {
            "models": ["app.models.user", "aerich.models"],
            "default_connection": "default",
        }
    },
}

