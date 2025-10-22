import streamlit as st

def login_page():
        st.title("로그인 페이지")
        st.subheader("🏎️ F1 레이싱 분석")   

        userId = st.text_input(
            label = "UserID",
            placeholder = "아이디를 입력해주세요",
            label_visibility = "collapsed" # label을 숨김 처리
        )

        password = st.text_input(
            label = "Password",
            type = "password",
            placeholder = "비밀번호를 입력해주세요",
            label_visibility = "collapsed" # label을 숨김 처리
        )
        login_button = st.button("Login", use_container_width=True, type="primary")
        sign_button = st.button("회원가입", use_container_width=True, key="signup_button")

        if login_button:
            response = login_user(userId, password) #서비스 로그인 함수 호출
            if response is None:
                st.error(f"로그인 실패: 서버 연결 불가")
            elif response.status_code == 200:
                user_data = response.json() #로그인 성공 시 사용자 데이터
                print(f"user_data: {user_data}") #디버깅용
                st.session_state.logged_in = True #로그인 상태로 변경
                st.session_state.user_id = user_data.get("userId") #세션에 사용자 아이디 저장 
                st.session_state.username = user_data.get("username") #세션에 사용자 이름 저장
                st.rerun()  # 로그인 상태가 변경되었으므로 페이지를 다시 렌더링합니다.
            else:
                error_data = response.json()
                st.error(error_data.get("detail", "로그인 실패"))

        if sign_button: #회원가입 버튼
            st.session_state.page = 'signup' # 보여줄 페이지를 'signup'으로 변경
            st.rerun() # 페이지를 다시 그려달라고 요청
            
if __name__ == "__main__":
    login_page()