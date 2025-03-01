from sqlalchemy import Column, Integer, ForeignKey, Float, String, TIMESTAMP, func
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    tickets = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default="Pending")  # Pending, Confirmed, Cancelled
    created_at = Column(TIMESTAMP, server_default=func.now())
