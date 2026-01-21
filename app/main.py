from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.db.base import TORTOISE_CONFIG

from app.api.v1.quote import router as quote_router # 별명
from app.api.v1.question import router as question_router # 별명


app = FastAPI(title="FastAPI Mini Project")

app.include_router(quote_router, prefix="/api/v1")
app.include_router(question_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Hello World! Database is connected."}

# DB 연결 설정 (이게 있어야 아까처럼 DB와 통신이 가능합니다)
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,  # 마이그레이션 도구(aerich)를 쓸 거니까 False!
    add_exception_handlers=True,
)