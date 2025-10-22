import streamlit as st
from run import (
    load_data, 
    get_top_n_counts, 
    create_yearly_wins_chart, 
    get_driver_profile_data, 
    create_wins_by_team_pie_chart,
    favorite_driver,  # API 호출을 위한 함수라고 가정합니다.
    login_user
)
from UI.sign_ui import sign_up_page

#==========================메인 페이지===========================
def main_page():
    # 앱이 처음 실행되거나 페이지가 새로고침 될 때 세션 상태 초기화
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if st.session_state.logged_in: #로그인 상태일 때
        show_dashboard()  # 대시보드 함수 호출
    else:
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

        if sign_button:
            st.session_state.page = 'signup' # 보여줄 페이지를 'signup'으로 변경
            st.rerun() # 페이지를 다시 그려달라고 요청

def logout():
    """세션 상태를 초기화하여 로그아웃을 처리하는 함수"""
    # st.session_state의 모든 키를 삭제하여 완벽하게 초기화
    for key in st.session_state.keys():
        del st.session_state[key]
    st.toast("로그아웃 되었습니다.")
    st.rerun()

#==========================대시보드 페이지===========================

def show_driver_profile(df, driver_name):
    """선택된 드라이버의 상세 프로필 정보를 시각화하는 함수"""
    st.header(f"👨‍🚀 드라이버 프로필: {driver_name}")

    # 1. 로직 함수를 호출하여 프로필 데이터 계산
    profile_data = get_driver_profile_data(df, driver_name)

    if profile_data is None:
        st.warning("선택한 드라이버의 우승 기록이 데이터에 없습니다.")
        return

    # 2. 주요 기록을 st.metric으로 시각적으로 강조하여 표시
    col1, col2, col3 = st.columns(3)
    col1.metric("통산 우승 횟수", f"{profile_data['total_wins']} 회")
    col2.metric("첫 우승 연도", f"{profile_data['first_win_year']} 년")
    col3.metric("마지막 우승 연도", f"{profile_data['last_win_year']} 년")
    
    st.divider()

    # 3. 팀별 우승 분포(파이 차트)와 전체 우승 기록(테이블)을 나란히 표시
    col4, col5 = st.columns([1, 1.5]) # 왼쪽이 약간 좁게
    with col4:
        st.subheader("소속 팀별 우승 분포")
        pie_chart_fig = create_wins_by_team_pie_chart(profile_data['wins_by_team_df'], driver_name)
        if pie_chart_fig:
            st.plotly_chart(pie_chart_fig, use_container_width=True)

    with col5:
        st.subheader("전체 우승 기록")
        # 표시할 컬럼만 선택하여 깔끔하게 보여주기
        display_cols = ['연도', '그랑프리', '팀', '서킷']
        st.dataframe(
            profile_data['all_wins_df'][display_cols],
            use_container_width=True,
            hide_index=True
        )

def show_dashboard():
    f1_df = load_data('f1.csv')

    # --- 사이드바 ---
    st.sidebar.write(f"{st.session_state.get('user_name', st.session_state.username)}님, 환영합니다!")
    st.sidebar.button("로그아웃", on_click=logout, use_container_width=True)
    st.sidebar.divider()
    
    st.sidebar.header("메뉴")
    analysis_option = st.sidebar.selectbox("분석 항목 선택:", ('전체 개요', '팀별 상세 분석', '드라이버별 상세 분석', '관심 드라이버'))

    # --- 메인 화면 ---
    st.title('🏎️ F1 레이싱 데이터 분석')

    if f1_df is None:
        st.error("데이터 파일('f1.csv')을 찾을 수 없습니다.")
        return

    # --- 페이지 렌더링 ---
    if analysis_option == '전체 개요':
        st.header("🏆 F1 역대 기록 TOP 15")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🏁 팀별 누적 우승")
            st.dataframe(get_top_n_counts(f1_df, '팀', 15))
        with col2:
            st.subheader("🥇 드라이버별 누적 우승")
            st.dataframe(get_top_n_counts(f1_df, '우승자', 15))

    elif analysis_option in ['팀별 상세 분석', '드라이버별 상세 분석']:
        is_team_analysis = analysis_option == '팀별 상세 분석'
        group_col = '팀' if is_team_analysis else '우승자'
        header_text = "팀별" if is_team_analysis else "드라이버별"
        
        st.header(f"🛠️ {header_text} 상세 분석")
        all_items = sorted(f1_df[group_col].unique())
        default_items = all_items[:3] if len(all_items) >= 3 else all_items
        selected_items = st.multiselect(f"분석할 {group_col} 선택 (최대 5개):", all_items, default=default_items)

        if not selected_items:
            st.warning(f"분석할 {group_col}을(를) 1개 이상 선택해주세요.")
        elif len(selected_items) > 5:
            st.warning(f"최대 5개의 {group_col}만 선택할 수 있습니다.")
        else:
            fig, filtered_data = create_yearly_wins_chart(f1_df, group_col, selected_items)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            with st.expander("세부 데이터 보기"):
                st.dataframe(filtered_data.sort_values('연도', ascending=False))

    elif analysis_option == '관심 드라이버':
        st.subheader("⭐ 내 대표 드라이버 설정")
        
        all_drivers = sorted(f1_df['우승자'].unique())
        # 로그인 시 API로부터 받아온 favorite_driver 정보를 사용
        current_favorite = st.session_state.get('favorite_driver') 
        
        default_index = all_drivers.index(current_favorite) if current_favorite in all_drivers else 0
        
        selected_driver = st.selectbox("대표 드라이버를 선택하세요:", all_drivers, index=default_index)

        if st.button("대표 드라이버로 저장", type="primary"):
            # API를 호출하여 서버에 저장
            response = favorite_driver(st.session_state.user_id, selected_driver) 
            if response and response.status_code == 200:
                # API 호출 성공 시 세션 상태도 업데이트
                st.session_state.favorite_driver = selected_driver
                st.success(f"'{selected_driver}' 선수를 대표 드라이버로 저장했습니다.")
                st.rerun()
            else:
                st.error("저장에 실패했습니다. 다시 시도해주세요.")

        st.divider()

        # 저장된 대표 드라이버가 있을 경우 프로필 페이지 함수 호출
        if st.session_state.get('favorite_driver'):
            show_driver_profile(f1_df, st.session_state.favorite_driver)
        else:
            st.info("대표 드라이버를 선택하고 저장하면 상세 프로필을 볼 수 있습니다.")


# 페이지 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'login' # 앱 시작 시 보여줄 기본 페이지

# st.session_state.page 값에 따라 적절한 페이지 함수를 호출
if st.session_state.page == 'login':
    main_page()
elif st.session_state.page == 'signup':
    sign_up_page()