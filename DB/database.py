from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite DB 연결 (파일 기반)
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite는 단일 스레드 제한이 있음
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
