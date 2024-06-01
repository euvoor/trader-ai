import uuid
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class HistoricalDataCache(Base):
    __tablename__ = "historical_data_cache"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    interval = Column(String, index=True, nullable=False)
    start = Column(String, index=True, nullable=False)
    end = Column(String, index=True, nullable=False)
    json_data = Column(JSONB, nullable=False)

def create_tables():
    Base.metadata.create_all(bind=engine)
