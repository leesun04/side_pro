import sqlite3
import os

def confirm_db(): #DB가 연결됐는지 확인하는 함수
    db_file = 'my_data.db'
    
    # #DB 파일이 없는 경우를 대비한 예외 처리
    # if not os.path.exists(db_file):
    #     print(f"오류: '{db_file}' 데이터베이스 파일이 존재하지 않습니다.")
    #     print("데이터를 먼저 추가해주세요.")
    #     return # 함수 종료

    # --- 1단계: 데이터베이스에 연결하기 ---
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        print("\n[1단계] 데이터베이스에 성공적으로 연결되었습니다.")

        # --- 2단계: 테이블이 존재하는지 확인 (없으면 생성) ---
        # 이 코드는 테이블이 없을 때를 대비한 안전장치입니다.
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            userId TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            username TEXT NOT NULL
        );
        """)
        
        # --- 추가된 부분: DB 안의 모든 데이터를 가져오기 ---
        print("\n[2단계] 저장된 모든 사용자 데이터를 조회합니다.")
        
        # 1. "users" 테이블에서 모든(*) 데이터를 선택(조회)하라고 명령
        cur.execute("SELECT userId, username FROM users;")
        
        # 2. 위에서 실행한 조회 결과를 모두(all) 가져와서(fetch) all_users 변수에 저장
        all_users = cur.fetchall()

        # --- 3단계: 가져온 데이터 출력하기 ---
        print("\n[3단계] 현재 DB에 저장된 내용입니다.")
        print("==================================================================================")
        print("USERID | username")
        print("----------------------------------------------------------------------------------")
        
        if not all_users:
            print(" -> 데이터가 비어있습니다.")
        else:
            for user in all_users:
                # user[0] = id, user[1] = username, user[2] = password_hash
                print(f" {user[0]:<2} | {user[1]:<8}")
        
        print("==================================================================================")

    # 'with' 구문을 사용했으므로 conn.close()는 자동으로 처리됩니다.
    print("\n[4단계] 작업 완료. 데이터베이스 연결은 자동으로 종료되었습니다.")


# --- 이 함수를 테스트하기 위한 실행 코드 ---
if __name__ == "__main__":
    # 만약 my_data.db 파일이 비어있다면, 아래와 같이 데이터를 먼저 추가해야 합니다.
    # (이전에 만들었던 'db_tutorial_password.py' 스크립트를 실행하면 데이터가 추가됩니다.)
    
    # 이제 DB 내용을 확인하는 함수를 호출합니다.
    confirm_db()

# # --- 3단계: 데이터 준비 및 암호화하여 넣기 (Insert) ---
# # 원본 사용자 이름과 비밀번호 데이터
# users_to_add = [
#     ('gildong', 'password123'),
#     ('chulsoo', 'chulsoo!@#'),
#     ('younghee', 'yh4321')
# ]

# # 암호화하여 저장할 데이터를 담을 리스트
# users_to_insert = []
# for username, password in users_to_add:
#     # 비밀번호를 sha256 방식으로 암호화
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     users_to_insert.append((username, hashed_password))
#     print(f" -> '{username}'의 비밀번호를 암호화했습니다.")

# # 암호화된 데이터들을 DB에 추가
# cur.executemany("INSERT INTO users (username, password_hash) VALUES (?, ?);", users_to_insert)
# print(f"\n[3단계] 암호화된 데이터 {len(users_to_insert)}개를 성공적으로 넣었습니다.")


# # --- 중요! 변경사항 저장하기 (Commit) ---
# conn.commit()
# print(" -> 변경사항이 실제 파일에 저장되었습니다.")


# # --- 4단계: 데이터 확인하기 (Read) ---
# print("\n[4단계] 저장된 모든 사용자 데이터를 확인합니다.")
# cur.execute("SELECT * FROM users;")
# all_users = cur.fetchall()
