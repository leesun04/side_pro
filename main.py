import streamlit as st
from UI.user_pages.login_ui import login_page
from UI.user_pages.sign_ui import sign_up_page

# 페이지 전체 설정
st.set_page_config(page_title="My App", layout="centered")

# 페이지 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'login' # 앱 시작 시 보여줄 기본 페이지


# st.session_state.page 값에 따라 적절한 페이지 함수를 호출
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    sign_up_page()
# elif st.session_state.page == 'some_other_page':
#     some_page_function()

# 로그인 성공 후 보여줄 메인 대시보드 페이지
elif st.session_state.logged_in:
    st.title("메인 대시보드")
    st.write(f"{st.session_state.user_name}님, 환영합니다! 여기가 메인 페이지입니다.")
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.rerun()
#streamlit run main.py --server.address 0.0.0.0 --server.port 8501 실행