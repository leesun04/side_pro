import streamlit as st
from services import services_login

def login_page():
    st.title("로그인 페이지")

    # 앱이 처음 실행되거나 페이지가 새로고침 될 때 세션 상태 초기화
    if 'logged_in' not in st.session_state: #로그인됐다는 거
        st.session_state.logged_in = False
    if 'userId' not in st.session_state: #로그인된 사용자가 있을대
        st.session_state.userId = None

    def logout(): #UI 로그아웃 함수 -> 이건 ui에서 처리해야해서 일로 뺌
        st.session_state.logged_in = False
        st.session_state.userId = None
        st.success("로그아웃 되었습니다.")

    #========================== UI 구성 ==========================
    if st.session_state.logged_in: #로그인 상태일 때
        st.write(f"{st.session_state.userId}님, 환영합니다!")
        if st.button("로그아웃", use_container_width=True, on_click=logout):
            pass  # 로그아웃 함수는 on_click에서 처리됩니다.
        
    else: #로그아웃 상태일 때
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
            response = services_login.login_user(userId, password) #서비스 로그인 함수 호출
            if response is None:
                st.error(f"로그인 실패: 서버 연결 불가")
            elif response.status_code == 200:
                user_data = response.json() #로그인 성공 시 사용자 데이터
                st.session_state.logged_in = True #로그인 상태로 변경
                st.session_state.userId = user_data.get("userId") #세션에 userId 저장
                st.rerun()  # 로그인 상태가 변경되었으므로 페이지를 다시 렌더링합니다.
            else:
                error_data = response.json()
                st.error(error_data.get("detail", "로그인 실패"))
        
        if sign_button:
            st.session_state.page = 'signup' # 보여줄 페이지를 'signup'으로 변경
            st.rerun() # 페이지를 다시 그려달라고 요청

