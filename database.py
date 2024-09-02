from sqlalchemy import create_engine, Column, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from databases import Database

DATABASE_URL = "sqlite:///./satellites.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

database = Database(DATABASE_URL)

class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    created_at = Column(DateTime)

Base.metadata.create_all(bind=engine)
