import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Login Page", layout="centered")

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
st.title("Login")

# 이메일 입력
email = st.text_input(
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

# 아이디 저장하기 체크박스
st.checkbox("아이디 저장하기")

# --- 버튼들 ---
login_button = st.button("Login", use_container_width=True, type="primary")
signup_button = st.button("회원가입", use_container_width=True, key="signup_button")

# --- 로그인 로직 ---
if login_button:
    if email and password:
        st.success(f"{email}님, 환영합니다!")
    else:
        st.error("이메일과 비밀번호를 모두 입력해주세요.")

# --- 회원가입 로직 ---
if signup_button:
    st.info("회원가입 페이지로 이동합니다. (기능 구현 필요)")