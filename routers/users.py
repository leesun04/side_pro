from fastapi import APIRouter, HTTPException, Depends, status, Form
from pydantic import BaseModel
import hashlib # 비밀번호 암호화
import sqlite3

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
db_PATH = "/mnt/nas4/lsj/side_project/DB/my_data.db" #DB 경로

@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="회원가입")
async def signup(userId: str = Form(...), password: str = Form(...), username: str = Form(...)):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user_to_insert = (userId, hashed_password, username)

    with sqlite3.connect(db_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (userId, password_hash, username) VALUES (?, ?, ?);", user_to_insert)
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 사용자입니다.",
            )
    return {"message": f"{username}님 회원가입 환영합니다!"}


@router.post("/login", summary="로그인")
async def login(userId: str = Form(...), password: str = Form(...)):
    with sqlite3.connect(db_PATH) as conn:
        cur = conn.cursor()
        # ✨ 2. 로그인 시 favorite 컬럼도 함께 조회
        sql = "SELECT userId, password_hash, username, favorite FROM users WHERE userId = ?;"
        cur.execute(sql, (userId,))
        user = cur.fetchone()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하는 사용자가 없습니다.",
            )
        
        stored_userId, stored_password_hash, username, favorite_driver = user
        hashed_input_password = hashlib.sha256(password.encode()).hexdigest()

        if hashed_input_password != stored_password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 틀렸습니다.",
            )
        
        # ✨ 3. 로그인 응답에 username과 favorite_driver를 함께 반환
        return {"message": "로그인 성공!", "username": username, "favorite_driver": favorite_driver, "userId": stored_userId}

# --- ✨ 4. 즐겨찾기 드라이버 업데이트를 위한 Pydantic 모델 ---
class FavoriteDriverUpdate(BaseModel):
    driver_name: str

# --- ✨ 5. 즐겨찾기 드라이버를 업데이트하는 API 엔드포인트 ---
@router.post("/{userId}/favorite", status_code=status.HTTP_200_OK, summary="대표 드라이버 저장")
async def update_favorite(userId: str, favorite_update: FavoriteDriverUpdate):
    with sqlite3.connect(db_PATH) as conn:
        cur = conn.cursor()
        # 사용자가 실제로 존재하는지 먼저 확인 (선택사항이지만 더 안전함)
        cur.execute("SELECT id FROM users WHERE userId = ?", (userId,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
            
        # favorite 컬럼 업데이트
        cur.execute("UPDATE users SET favorite = ? WHERE userId = ?", (favorite_update.driver_name, userId))

    return {"message": "대표 드라이버가 성공적으로 저장되었습니다.", "favorite_driver": favorite_update.driver_name}
