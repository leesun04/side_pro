import requests

def login_user(userId, password): #로그인api 연결 함수
    
    API_URL = "" 

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
    
    API_URL = ""   
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
    API_URL = ""
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