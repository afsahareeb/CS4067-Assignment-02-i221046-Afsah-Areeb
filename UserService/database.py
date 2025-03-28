from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres_user:1234@postgres-user:5432/event_booking"

engine = create_engine(DATABASE_URL) # establis connection with database
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # to interact with db(read/write)
Base = declarative_base() # to create models
metadata = MetaData() # stores schema information

# Create tables
def init_db():
    from models import User  # Import your models
    Base.metadata.create_all(bind=engine)  # Creates tables automatically