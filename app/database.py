from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://pg:pg@postgres/api"


settings = Settings()

# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./sqlite.db"

# The part `connect_args={"check_same_thread": False}` is needed only for SQLite
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
