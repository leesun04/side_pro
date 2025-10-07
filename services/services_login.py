#로그인 화면 api 연결 로직
import requests

API_URL = "http://203.252.147.196:8002/users" 

def login_user(userId, password): #로그인api 연결 함수
    try:
        response = requests.post(
            f"{API_URL}/login",
            data={"userId": userId, "password": password}
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during login request: {e}")
        return None
    
def signup_user(userId, password): #회원가입 api 연결 함수
    try:
        response = requests.post(
            f"{API_URL}/signup",
            data={"userId": userId, "password": password}
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during signup request: {e}")
        return None