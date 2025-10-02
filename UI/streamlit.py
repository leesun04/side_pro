import streamlit as st
import pandas as pd

# Initialize session state if not already done
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''

def main_dashboard():
    st.set_page_config(page_title="FitSpot Dashboard", page_icon="💪", layout="wide")

    # If NOT logged in, show login form
    if not st.session_state['logged_in']:
        st.warning("메인 화면을 보려면 로그인이 필요합니다.")
        
        col1, col2, col3 = st.columns([1,1.5,1])
        with col2:
            with st.form("login_form"):
                st.header("로그인")
                username = st.text_input("사용자 이름")
                password = st.text_input("비밀번호", type="password")
                
                submitted = st.form_submit_button("로그인")

                if submitted:
                    # Dummy authentication
                    if username and password: # In a real app, you'd check this against a DB
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.rerun()
                    else:
                        st.error("사용자 이름과 비밀번호를 입력해주세요.")   # st.bar_chart는 pandas DataFrame이나 numpy array와 함께 사용하는 것이 가장 좋습니다.
                        
        
        st.info("계정이 없으신가요? 왼쪽 사이드바에서 '회원가입'을 선택하세요.")

    # If LOGGED IN, show the dashboard
    else:
        # Hide the sign-up page link from the sidebar
        st.markdown("""
            <style>
                div[data-testid="stSidebarNav"] ul li a[href="/sign"] {
                    display: none;
                }
            </style>
        """, unsafe_allow_html=True)

        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title(f"💪 {st.session_state['username']}님의 대시보드")
            st.subheader("오늘도 목표를 향해 달려보세요!")
        with col2:
            if st.button("로그아웃"):
                st.session_state['logged_in'] = False
                st.session_state['username'] = ''
                st.rerun()

        st.markdown("---")

        # Dashboard Metrics
        st.header("오늘의 현황")
        col1, col2, col3 = st.columns(3)
        col1.metric("오늘 한 운동 (개)", "3", "1")
        col2.metric("총 운동 시간 (분)", "45", "5")
        col3.metric("소모 칼로리 (kcal)", "320", "-20")

        st.markdown("---")

        # Placeholder for other content
        st.header("나의 활동")
        # 가장 기본적인 Streamlit 막대 그래프로 되돌립니다.
        # x축 레이블은 숫자 인덱스로 표시되며, 공간이 부족하면 회전될 수 있습니다.
        # st.bar_chart({"주간 활동량": [10, 5, 2, 8, 1, 9, 3]})
        
        # Pandas DataFrame을 사용하여 x축에 의미있는 레이블을 부여하는 것이 가장 좋습니다.
        chart_data = pd.DataFrame(
           [10, 5, 2, 8, 1, 9, 3],
           index=['월', '화', '수', '목', '금', '토', '일'],
           columns=["주간 활동량"]
        )
        st.bar_chart(chart_data)
        #st.info("왼쪽 사이드바에서 다른 메뉴로 이동할 수 있습니다.")


if __name__ == "__main__":
    main_dashboard()