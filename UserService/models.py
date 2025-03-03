from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, func, Float
from database import Base

class User(Base):
    __tablename__ = "users" # table name in postgresql

    # columns in the table
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    balance = Column(Float, default=1000.0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
