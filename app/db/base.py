import os
from dotenv import load_dotenv
from app.core.config import settings

# 파일명을 명시적으로 지정
load_dotenv(".env.dev")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TORTOISE_CONFIG = {
    "connections": {
        "default": settings.DATABASE_URL
    },
    "apps": {
        "models": {
            # 마이그레이션할 모델 경로들
            # 주의: 파일명이 실제로 app/models/user.py 인지 확인하세요!
            "models": ["app.models.user", "aerich.models"],
            "default_connection": "default",
        }
    },
}