from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

fake_db = {} #임시 데이터베이스
class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="회원가입")
async def signup(user: UserIn):
    if user.username in fake_db:
        print("User already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 사용자입니다.",
        )
    fake_db[user.username] = {"password":user.password}
    print(fake_db)
    return {"message": f"{user.username}님 회원가입 환영한다!!!!!"}