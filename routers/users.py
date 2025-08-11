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

@router.post("/login", response_model=UserOut, summary="로그인")
async def login(user: UserIn):
    if user.username not in fake_db:
        print("User does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자입니다.",
        )
    if fake_db[user.username]["password"] != user.password:
        print("Incorrect password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 틀렸습니다.",
        )
    print(fake_db)
    return {"username": user.username}