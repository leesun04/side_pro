from fastapi import FastAPI
from routers import users

app = FastAPI(
    title="사이드 포폴 사용자 DB API용"
)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"meaage": "Fast API 회원가입 예제임"}