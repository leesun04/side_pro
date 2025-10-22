import streamlit as st


# 페이지 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'login' # 앱 시작 시 보여줄 기본 페이지

# st.session_state.page 값에 따라 적절한 페이지 함수를 호출
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    sign_up_page()