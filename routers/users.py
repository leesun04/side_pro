from fastapi import APIRouter, HTTPException, Depends, status, Form

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

fake_db = {} #임시 데이터베이스

@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="회원가입")
async def signup(username: str = Form(...), password: str = Form(...)):
    if username in fake_db:
        print("User already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 사용자입니다.",
        )
    fake_db[username] = {"password":password}
    print(fake_db)
    return {"message": f"{username}님 회원가입 환영한다!!!!!"}

@router.post("/login", summary="로그인")
async def login(username: str = Form(...), password: str = Form(...)):
    if username not in fake_db:
        print("User does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자입니다.",
        )
    if fake_db[username]["password"] != password:
        print("Incorrect password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 틀렸습니다.",
        )
    print(fake_db)
    return {"username": username}

@router.post("/logout", summary="로그아웃")
async def logout(username: str = Form(...)):
    if username not in fake_db:
        print("User does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자입니다.",
        )
    del fake_db[username] # 임시 데이터베이스에서 사용자 삭제
    print(f"{username}님 로그아웃 되었습니다.")
    return {"message": f"{username}님 로그아웃 되었습니다."}