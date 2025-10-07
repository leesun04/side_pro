from fastapi import APIRouter, HTTPException, Depends, status, Form

import hashlib # 비밀번호 암호화
import sqlite3

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
db_PATH = "/mnt/nas4/lsj/side_project/DB/my_data.db" #DB 경로

@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="회원가입")
async def signup(userId: str = Form(...), password: str = Form(...), username: str = Form(...)):
   
    hashed_password = hashlib.sha256(password.encode()).hexdigest() # 비밀번호 암호화
    user_to_insert = (userId, hashed_password, username) #DB에 넣기전 튜플

    with sqlite3.connect(db_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (userId, password_hash, username) VALUES (?, ?, ?);", user_to_insert)
            #execute란 명령어를 실행하라고 하는거임
            
            # conn.commit() # -> 왜냐하면!!!!! with 구문 사용 시 자동으로 commit/close 되기 때문에 주석처리
        except sqlite3.IntegrityError:
            # 중복 사용자가 있을때 발생하는 것
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 사용자입니다.",
            )
    return {"message": f"{username}님 회원가입 환영한다!!!!!"}

#===========================================================================================================================

@router.post("/login", summary="로그인")
async def login(userId: str = Form(...), password: str = Form(...)):
    with sqlite3.connect(db_PATH) as conn:
        cur = conn.cursor()
        sql = "SELECT userId, password_hash FROM users WHERE userId = ?;" #해당 열들을 선택하겠다는 의미 -> userId와 password를 가져올거임ㅋ
        #WHERE userId = ? 이거는 조건에 맞는 데이터만 가져오겠다는 필터
    
        cur.execute(sql, (userId,)) #명령어 실행 -> userId를 조회하기 시작
        user = cur.fetchone() #조회한 결과를 가져오기 (없다면 None 반환)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하는 사용자가 없습니다..",
            )
        stored_userId, stored_password_hash = user #DB에 있는 userId와 password_hash를 각각 변수에 저장
        hashed_input_password = hashlib.sha256(password.encode()).hexdigest() #입력받은 비밀번호 암호화
        
        if hashed_input_password != stored_password_hash: #입력받은 비밀번호랑 DB에 있는 비밀번호랑 비교하기
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 틀렸습니다..",
            )
        
        return {"message": "로그인 성공!", "userId": stored_userId} #아이디 반환 (토큰은 사용하지말자... 어렵다..)
