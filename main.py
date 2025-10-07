from fastapi import FastAPI
from routers import users

app = FastAPI(
    title="사용자 DB API용"
)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"meaage": "Fast API 회원가입 예제임"}

#uvicorn main:app --reload --port 8002 --host 0.0.0.0 -> 이거 1번서버에서 실행시키는 명령어