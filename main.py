from fastapi import FastAPI

# 변수 이름이 반드시 'app'이어야 uvicorn main:app과 매칭됩니다.
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}