from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres_event:1234@postgres-event:5432/Events"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
metadata = MetaData()

def init_db():
    from models import Event  # Import your models
    Base.metadata.create_all(bind=engine)