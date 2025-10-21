import pandas as pd
import requests


def load_data(filepath):
    """CSV 파일을 불러오고, 인코딩 문제 처리 및 기본 데이터 정제를 수행하는 함수"""
    try:
        df = pd.read_csv(filepath)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding='cp949')
        except Exception as e:
            print(f"다양한 인코딩으로 파일을 읽는 데 실패했습니다: {e}")
            return None
    except FileNotFoundError:
        print(f"'{filepath}' 파일을 찾을 수 없습니다. app.py와 같은 폴더에 파일이 있는지 확인해주세요.")
        return None
        
    return df

def login_user(userId, password): #로그인api 연결 함수
    
    API_URL = "http://203.252.147.196:8002/users" 

    try:
        response = requests.post(
            f"{API_URL}/login",
            data={"userId": userId, "password": password}
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during login request: {e}")
        return None
    
def signup_user(userId, password, username): #회원가입 api 연결 함수
    
    API_URL = "http://203.252.147.196:8002/users"   
    try:
        response = requests.post(
            f"{API_URL}/signup",
            data={"userId": userId, "password": password, "username": username}
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during signup request: {e}")
        return None

def load_data(filepath):
    """CSV 파일을 불러와 인코딩 문제 처리 및 기본 데이터 정제를 수행하는 함수"""
    try:
        df = pd.read_csv(filepath)
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding='cp949')
    except FileNotFoundError:
        return None # 파일이 없으면 None을 반환
    
    if '연도' in df.columns:
        df['연도'] = pd.to_numeric(df['연도'], errors='coerce')
        df.dropna(subset=['연도'], inplace=True)
        df['연도'] = df['연도'].astype(int)

    return df

def get_top_n_counts(df, column_name, n=15):
    """주어진 컬럼의 상위 n개 카운트를 반환하는 함수"""
    if df is not None and column_name in df.columns:
        return df[column_name].value_counts().head(n)
    return pd.Series() # 데이터가 없으면 빈 Series 반환

def prepare_yearly_wins_chart_data(df, group_by_column, selected_items):
    """
    선택된 항목에 대해 연도별 우승 횟수 데이터를 차트 형식에 맞게 가공하는 함수.
    
    Returns:
        tuple: (차트용 데이터프레임, 차트의 y축 컬럼 리스트, 필터링된 원본 데이터프레임)
    """
    if df is None or not selected_items:
        return pd.DataFrame(), [], pd.DataFrame()

    filtered_df = df[df[group_by_column].isin(selected_items)]
    
    if filtered_df.empty:
        return pd.DataFrame(), [], pd.DataFrame()

    yearly_wins = filtered_df.groupby(['연도', group_by_column]).size().unstack(fill_value=0)
    
    # 차트용 데이터프레임 생성
    chart_df = yearly_wins.reset_index()
    chart_df['연도'] = pd.to_datetime(chart_df['연도'], format='%Y')
    
    return chart_df, yearly_wins.columns.tolist(), filtered_df

