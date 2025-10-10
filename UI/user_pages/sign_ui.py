import streamlit as st
from services import services_login

def sign_up_page():
    # --- CSS 스타일 ---
    # 페이지의 모든 커스텀 스타일을 한 곳에 모아서 관리합니다.
    st.markdown("""
    <style>
    /* 'st-emotion-cache-xxx'와 같은 자동 생성 클래스 이름을 무시하고 data-testid를 사용합니다. */
    /* 'stButton'은 Streamlit 버튼의 data-testid 기본값입니다. */
    /* 'signup_button'은 우리가 지정한 key 값입니다. */
    [data-testid="stButton"] > button[data-testid="baseButton-secondary"] {
        background-color: #28a745; /* 초록색 */
        color: white;
    }
    </style>
    """, unsafe_allow_html=True) # unsafe_allow_html=True 옵션을 사용하여 HTML/CSS가 적용되도록 합니다.

    # --- UI 구성 ---
    st.title("회원가입")

    # 아이디 입력
    userId = st.text_input(
        label="UserID",
        placeholder="아이디",
        label_visibility="collapsed" # label을 숨김 처리
    )

    # 비밀번호 입력
    password = st.text_input(
        label="Password",
        type="password",
        placeholder="비밀번호",
        label_visibility="collapsed" # label을 숨김 처리
    )

    username = st.text_input(
        label="Username",
        placeholder="이름",
        label_visibility="collapsed" # label을 숨김 처리
    )

    # --- 버튼들 ---
    signup_button = st.button("회원가입 완료", use_container_width=True, type="primary")
    back_button = st.button("로그인 페이지로 돌아가기", use_container_width=True)

    # --- 회원가입 로직 ---
    if signup_button:
        if not userId or not password or not username:
            st.error("모든 필드를 입력해주세요.")
            return
        response = services_login.signup_user(userId, password, username)
        if response is None:
            st.error("회원가입 실패: 서버 연결 불가")
            return
        elif response.status_code == 201:
            st.session_state.page = 'login' # 로그인 페이지로 상태 변경
            st.rerun()
            st.success("회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.")
        else:
            error_data = response.json()
            st.error(error_data.get("detail", "회원가입 실패"))
    if back_button:
        st.session_state.page = 'login' # 로그인 페이지로 상태 변경
        st.rerun()