from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# import database

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./sqlite.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

# The part `connect_args={"check_same_thread": False}` is needed only for SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# database = databases.Database(DATABASE_URL)
# metadata = sqlalchemy.MetaData()

# carsTbl = sqlalchemy.Table(
#     "cars",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("make_", sqlalchemy.String),
#     sqlalchemy.Column("model", sqlalchemy.String),
#     sqlalchemy.Column("rating", sqlalchemy.Integer),
# )

# metadata.create_all(engine)
# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
