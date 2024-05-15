from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings


settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.get_db_connection_string()

pool_size = settings.db_pool_size
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=pool_size, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
