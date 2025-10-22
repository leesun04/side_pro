import sqlite3
import os

# def confirm_db(): #DB가 연결됐는지 확인하는 함수
#     db_file = 'my_data.db'
    
#     # #DB 파일이 없는 경우를 대비한 예외 처리
#     # if not os.path.exists(db_file):
#     #     print(f"오류: '{db_file}' 데이터베이스 파일이 존재하지 않습니다.")
#     #     print("데이터를 먼저 추가해주세요.")
#     #     return # 함수 종료

#     # --- 1단계: 데이터베이스에 연결하기 ---
#     with sqlite3.connect(db_file) as conn:
#         cur = conn.cursor()
#         print("\n[1단계] 데이터베이스에 성공적으로 연결되었습니다.")

#         # --- 2단계: 테이블이 존재하는지 확인 (없으면 생성) ---
#         # 이 코드는 테이블이 없을 때를 대비한 안전장치입니다.
#         cur.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             userId TEXT NOT NULL UNIQUE,
#             password_hash TEXT NOT NULL,
#             username TEXT NOT NULL,
#             favorite TEXT
#         );
#         """)
        
#         # --- 추가된 부분: DB 안의 모든 데이터를 가져오기 ---
#         print("\n[2단계] 저장된 모든 사용자 데이터를 조회합니다.")
        
#         # 1. "users" 테이블에서 모든(*) 데이터를 선택(조회)하라고 명령
#         cur.execute("SELECT userId, username FROM users;")
        
#         # 2. 위에서 실행한 조회 결과를 모두(all) 가져와서(fetch) all_users 변수에 저장
#         all_users = cur.fetchall()

#         # --- 3단계: 가져온 데이터 출력하기 ---
#         print("\n[3단계] 현재 DB에 저장된 내용입니다.")
#         print("==================================================================================")
#         print("USERID | username")
#         print("----------------------------------------------------------------------------------")
        
#         if not all_users:
#             print(" -> 데이터가 비어있습니다.")
#         else:
#             for user in all_users:
#                 # user[0] = id, user[1] = username, user[2] = password_hash
#                 print(f" {user[0]:<2} | {user[1]:<8} | {user[2]} ")
        
#         print("==================================================================================")

#     # 'with' 구문을 사용했으므로 conn.close()는 자동으로 처리됩니다.
#     print("\n[4단계] 작업 완료. 데이터베이스 연결은 자동으로 종료되었습니다.")


# # --- 이 함수를 테스트하기 위한 실행 코드 ---
# if __name__ == "__main__":
#     # 만약 my_data.db 파일이 비어있다면, 아래와 같이 데이터를 먼저 추가해야 합니다.
#     # (이전에 만들었던 'db_tutorial_password.py' 스크립트를 실행하면 데이터가 추가됩니다.)
    
#     # 이제 DB 내용을 확인하는 함수를 호출합니다.
#     confirm_db()


# --- 설정 ---
# 실제 DB 파일 경로를 여기에 입력하세요.
db_file = "/mnt/nas4/lsj/side_project/DB/my_data.db" 

def confirm_db_contents():
    """데이터베이스에 연결하여 users 테이블의 모든 내용을 확인하는 함수"""
    try:
        with sqlite3.connect(db_file) as conn:
            cur = conn.cursor()
            print(f"\n[성공] '{db_file}' 데이터베이스에 연결되었습니다.")

            # --- ✨ 1. SELECT 구문 수정 ---
            # print문에서 출력할 모든 컬럼(id, userId, username, favorite)을 조회합니다.
            try:
                cur.execute("SELECT id, userId, username, favorite FROM users;")
                all_users = cur.fetchall()
            except sqlite3.OperationalError as e:
                print(f"\n[오류] 테이블을 조회하는 중 문제가 발생했습니다: {e}")
                print(" -> 'users' 테이블이나 컬럼 이름이 올바른지 확인해주세요.")
                return

            # --- 2. 가져온 데이터 출력하기 (안전하게) ---
            print("\n--- 현재 DB에 저장된 사용자 정보 ---")
            # 헤더를 출력할 때 favorite도 추가합니다.
            print(f" {'ID':<4} | {'USERID':<15} | {'USERNAME':<15} | {'FAVORITE DRIVER'} ")
            print("-" * 60)
            
            if not all_users:
                print(" -> 데이터가 비어있습니다.")
            else:
                for user in all_users:
                    # user 튜플은 이제 (id, userId, username, favorite) 4개의 값을 가집니다.
                    # user[0] = id, user[1] = userId, user[2] = username, user[3] = favorite
                    
                    # favorite 값이 비어있는 경우(None)를 처리하여 더 안정적으로 만듭니다.
                    user_id = user[0]
                    user_userid = user[1]
                    user_username = user[2]
                    user_favorite = user[3] if user[3] is not None else "지정되지 않음"

                    print(f" {user_id:<4} | {user_userid:<15} | {user_username:<15} | {user_favorite} ")
            
            print("-" * 60)

    except sqlite3.Error as e:
        print(f"\n[오류] 데이터베이스 연결 또는 작업 중 에러가 발생했습니다: {e}")

if __name__ == "__main__":
    confirm_db_contents()