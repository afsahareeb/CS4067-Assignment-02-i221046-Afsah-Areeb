from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Event

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
"""
@router.post("/events/{event_id}/register")
def register_for_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Assuming we have a logged-in user (hardcoded for now)
    user_id = 1  # TODO: Replace with actual logged-in user ID

    db.execute("INSERT INTO event_attendees (event_id, user_id) VALUES (:event_id, :user_id)", {"event_id": event_id, "user_id": user_id})
    db.commit()
    return {"message": "Registered for event!"}

@router.post("/events/{event_id}/book")
def book_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Assuming user ID is available (for now, hardcoded as 1)
    user_id = 1  # TODO: Replace with actual logged-in user ID

    db.execute("INSERT INTO event_attendees (event_id, user_id) VALUES (:event_id, :user_id)", 
               {"event_id": event_id, "user_id": user_id})
    db.commit()
    return {"message": "Event booked successfully!"}


@router.get("/eventDashboard/")
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events
"""

@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    for event in events:
        print(f"Event ID: {event.id}, Tickets: {event.num_tickets}, Price: {event.ticket_price}")
    return [
        {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "location": event.location,
            "date": event.date,
            "num_tickets": event.num_tickets,  # ✅ Ensure tickets are included
            "ticket_price": event.ticket_price if event.ticket_price else 0.0  # ✅ Prevent undefined values
        }
        for event in events
    ]
