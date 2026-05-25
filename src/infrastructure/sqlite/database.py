from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATABASE_URL = f"sqlite:///{BASE_DIR}/sqlite.db".replace("\\", "/")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

expire_on_commit=False
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

Base = declarative_base()

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        session.close()
