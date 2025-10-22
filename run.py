import pandas as pd
import requests
import plotly.express as px 

import subprocess
import sys
import os
import webbrowser
import time

def install_and_run():
    """
    Streamlit 실행
    """
    try:
        #requirements.txt 파일 경로 확인
        req_path = 'requirements/requirements.txt'
        if not os.path.exists(req_path):
            # 'requirements' 폴더가 없는 경우를 대비해 상위 폴더도 확인
            req_path = 'requirements.txt'
            if not os.path.exists(req_path):
                print("ERROR: 'requirements.txt' 또는 'requirements/requirements.txt' 파일을 찾을 수 없습니다.")
                return # 함수 종료

        # requirements.txt를 이용해 라이브러리 설치
        print("Checking and installing required libraries...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_path]) #라이브러리 설치
        print("✅ Libraries are ready.")

        # Streamlit 서버 실행 (포트 8501 지정)
        print("Starting Streamlit server")
        command = [ # 서버 실행 명령어
            sys.executable, 
            "-m", "streamlit", "run", "run_ui.py", 
            "--server.port", "8501"
        ]
        server_process = subprocess.Popen(command) #서버 프로세스 시작
        
        # 4단계: 웹 브라우저 열기 (대기 시간 증가)
        print("Waiting for server to start...")
        time.sleep(5) # 서버가 켜질 시간 (5초)
        webbrowser.open("http://localhost:8501") #기본 브라우저로 열기
        
        # 서버가 종료될 때까지 기다립니다.
        server_process.wait()

    except subprocess.CalledProcessError as e:
        print(f"🚨 라이브러리 설치에 실패했습니다: {e}")
    except FileNotFoundError:
        print("🚨 ERROR: 'run_ui.py' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"🚨 An error occurred: {e}")

def login_user(userId, password): #로그인api 연결 함수
    
    API_URL = "http://203.252.147.196:8002/users" 

    try:
        response = requests.post( #api 호출
            f"{API_URL}/login",
            data={"userId": userId, "password": password} #전달 데이터
        )
        return response #응답 반환
    except requests.exceptions.RequestException as e:
        print(f"Error during login request: {e}")
        return None
    
def signup_user(userId, password, username): #회원가입 api 연결 함수
    
    API_URL = "http://203.252.147.196:8002/users"   
    try:
        response = requests.post( #api 호출
            f"{API_URL}/signup",
            data={"userId": userId, "password": password, "username": username} #전달 데이터
        )
        return response #응답 반환
    except requests.exceptions.RequestException as e:
        print(f"Error during signup request: {e}")
        return None

def favorite_driver(userId, driver_name): #즐겨찾기 드라이버 저장 함수
    API_URL = "http://203.252.147.196:8002/users"
    print(f"Updating favorite driver for userId: {userId} to {driver_name}") #디버깅용
    try:
        response = requests.post( #api 호출
            f"{API_URL}/{userId}/favorite",
            json={"driver_name": driver_name} #전달 데이터
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during favorite driver request: {e}")
        return None

def load_data(filepath):
    """CSV 파일을 불러와 인코딩 문제 처리 및 기본 데이터 정제를 수행하는 함수"""
    try:
        df = pd.read_csv(filepath) #기본 인코딩 시도
    except UnicodeDecodeError: #인코딩 오류 시
        df = pd.read_csv(filepath, encoding='cp949') #cp949 인코딩 시도
    except FileNotFoundError: #파일이 없을 때
        return None

    for col in ['우승자', '팀']: #문자열 컬럼의 ? 제거 및 공백 제거
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('?', '', regex=False).str.strip() #'?' 문자 제거 및 공백 제거
    
      
    if '연도' in df.columns: #연도 컬럼 정제
        df['연도'] = pd.to_numeric(df['연도'], errors='coerce') #숫자가 아닌 값은 NaN으로 변환
        df.dropna(subset=['연도'], inplace=True) #NaN 행 제거
        df['연도'] = df['연도'].astype(int) #정수형으로 변환
        df = df[df['연도'] >= 1950].copy() #1950년 이후 데이터만 필터링
    return df

def get_top_n_counts(df, column_name, n=15): #특정 컬럼에서 상위 n개의 값과 그 개수를 반환하는 함수
    if df is not None and column_name in df.columns: # 데이터프레임과 컬럼이 유효한지 확인
        return df[column_name].value_counts().head(n) #상위 n개 값과 개수 반환
    return pd.Series() #빈 시리즈 반환

def create_yearly_wins_chart(df, group_by_column, selected_items): #선택된 항목들의 연도별 우승 횟수 막대 차트 생성 함수
    """
    선택된 항목에 대한 연도별 우승 횟수를 Plotly 막대 차트로 생성하는 함수.
    
    Args:
        df (pd.DataFrame): 전체 F1 데이터프레임.
        group_by_column (str): '팀' 또는 '우승자'.
        selected_items (list): 사용자가 선택한 팀 또는 드라이버 리스트.
        
    Returns:
        tuple: (Plotly Figure 객체, 필터링된 원본 데이터프레임)
    """
    if df is None or not selected_items: #데이터프레임이 없거나 선택된 항목이 없으면
        return None, pd.DataFrame() #빈 값 반환

    filtered_df = df[df[group_by_column].isin(selected_items)] #선택된 항목으로 필터링
    
    if filtered_df.empty: #필터링 결과가 없으면
        return None, pd.DataFrame() #빈 값 반환

    # 차트용 데이터 집계
    yearly_wins = filtered_df.groupby(['연도', group_by_column]).size().reset_index(name='우승 횟수') #연도 및 그룹별 우승 횟수 집계
    
    # 툴팁에 표시될 라벨 이름을 지정
    labels_map = {
        '우승 횟수': '우승 횟수', # y축 라벨
        '연도': '연도',          # x축 라벨
        group_by_column: '팀' if group_by_column == '팀' else '드라이버' # 범례(color) 라벨
    }

    # Plotly Express로 막대 차트 생성
    fig = px.bar(
        yearly_wins, # 데이터프레임
        x='연도', # x축
        y='우승 횟수', # y축
        color=group_by_column,  # 이 컬럼 기준으로 막대 색을 다르게 함
        labels=labels_map,      # 라벨 매핑
        title=f"'{', '.join(selected_items)}'의 연도별 우승 횟수" # 차트 제목
    )
    
    return fig, filtered_df 

def get_driver_profile_data(df, driver_name):
    """특정 드라이버의 모든 관련 데이터를 계산하고 반환하는 함수"""
    if df is None or driver_name not in df['우승자'].values: # 데이터프레임이 없거나 드라이버가 없으면
        return None

    driver_df = df[df['우승자'] == driver_name].copy() #해당 드라이버 데이터 필터링
    
    total_wins = len(driver_df) #총 우승 횟수
    first_win_year = driver_df['연도'].min() #최초 우승 연도
    last_win_year = driver_df['연도'].max() #최신 우승 연도
    
    wins_by_team = driver_df['팀'].value_counts().reset_index() #팀별 우승 횟수 집계
    wins_by_team.columns = ['팀', '우승 횟수'] #컬럼명 변경
    
    profile_data = { # 드라이버 프로필 데이터 딕셔너리
        "total_wins": total_wins, #총 우승 횟수
        "first_win_year": first_win_year, #최초 우승 연도
        "last_win_year": last_win_year, #최신 우승 연도
        "wins_by_team_df": wins_by_team, #팀별 우승 횟수 데이터프레임
        "all_wins_df": driver_df.sort_values('연도', ascending=False) #해당 드라이버의 모든 우승 기록 데이터프레임
    }
    return profile_data #프로필 데이터 반환

def create_wins_by_team_pie_chart(wins_by_team_df, driver_name):
    """팀별 우승 횟수 데이터를 받아 파이 차트를 생성하는 함수"""
    if wins_by_team_df.empty: #데이터프레임이 비어있으면
        return None
        
    fig = px.pie( #파이 차트 생성
        wins_by_team_df, #데이터프레임
        names='팀', #파이 조각 이름
        values='우승 횟수', #파이 조각 값
        title=f'{driver_name} 선수의 팀별 우승 분포', #차트 제목
        hole=0.3 # 도넛 모양으로 만들기 
    )
    fig.update_traces(textposition='inside', textinfo='percent+label') #파이 조각 안에 퍼센트와 라벨 표시
    return fig


if __name__ == "__main__":
    install_and_run()