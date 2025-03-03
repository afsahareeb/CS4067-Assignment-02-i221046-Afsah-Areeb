from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Event
from fastapi import FastAPI

app = FastAPI()

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

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
            "num_tickets": event.num_tickets,
            "ticket_price": event.ticket_price if event.ticket_price else 0.0
        }
        for event in events
    ]

@router.get("/events/{event_id}/availability")
def check_availability(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return {
        "available_tickets": event.num_tickets,
        "ticket_price": event.ticket_price
    }
