from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./sqlite.db"
DATABASE_URL = "postgresql://pg:pg@postgres/api"

# The part `connect_args={"check_same_thread": False}` is needed only for SQLite
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
