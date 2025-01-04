from dotenv import load_dotenv
from sqlmodel import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

load_dotenv()

DB_PASSWORD = getenv('DATABASE_PASSWORD')
DB_USER = getenv('DATABASE_USER')
DB_NAME = getenv('DATABASE_NAME')
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

