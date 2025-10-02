import streamlit as st
import time

def signup_page():
    # Page config should be set on the main page, but can be set here for standalone running
    # st.set_page_config(page_title="FitSpot Seoul - 회원가입", page_icon="💪", layout="wide")

    # Centering the content
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.title("FitSpot Seoul 회원가입")
        st.subheader("새로운 계정을 만들어 FitSpot의 모든 기능을 활용해보세요.")
        st.markdown("---")

        with st.form("signup_form", clear_on_submit=True):
            st.markdown("#### 📝 계정 정보")
            username = st.text_input("사용자 이름", placeholder="사용자 이름을 입력하세요")
            email = st.text_input("이메일", placeholder="이메일 주소를 입력하세요")
            
            st.markdown("#### 🔒 비밀번호")
            password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            confirm_password = st.text_input("비밀번호 확인", type="password", placeholder="비밀번호를 다시 입력하세요")

            st.markdown("---")
            
            submitted = st.form_submit_button("✨ 가입하고 시작하기")

            if submitted:
                if not all([username, email, password, confirm_password]):
                    st.error("모든 필드를 빠짐없이 입력해주세요.")
                elif password != confirm_password:
                    st.error("비밀번호가 일치하지 않습니다. 다시 확인해주세요.")
                else:
                    st.success(f"🎉 환영합니다, {username}님! 회원가입이 성공적으로 완료되었습니다.")
                    st.info("잠시 후 메인 화면으로 이동합니다.")
                    st.balloons()

                    # Set session state to log the user in
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    
                    time.sleep(2) # Give user time to see the message
                    st.switch_page("streamlit.py") # Redirect to the main page

if __name__ == "__main__":
    signup_page()
