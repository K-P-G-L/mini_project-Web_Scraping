from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.db.base import TORTOISE_CONFIG

app = FastAPI(title="FastAPI Mini Project")


@app.get("/")
async def read_root():
    return {"message": "Database is connected."}


# DB 연결 설정 (이게 있어야 아까처럼 DB와 통신이 가능합니다)
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,  # 마이그레이션 도구(aerich)를 쓸 거니까 False!
    add_exception_handlers=True,
)
