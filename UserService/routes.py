import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from pydantic import BaseModel
import requests
from fastapi import APIRouter, HTTPException 
from fastapi import FastAPI

app = FastAPI()

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create a new user
@router.post("/users/") # create API that accepts POST requests
def create_user(first_name: str, last_name: str, email: str, password: str, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == email).first() # db.query(User) gets all users from the database filter(User.email == email) filters the users based on the email. first() returns the first user that matches the filter
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        db_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password)
        db.add(db_user)
        db.commit() # save the user to the database
        db.refresh(db_user) # refresh the user object to get the updated id
        return db_user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or user.password_hash != request.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful!", "user_email": user.email, "user_id": user.id}


class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    balance: float

@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    db_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password_hash=request.password,
        balance=request.balance
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User created successfully!", "user_email": db_user.email, "user_id": db_user.id}



EVENT_SERVICE_URL = "http://127.0.0.1:8000/events"
@router.get("/user/events")
def get_available_events():
    try:
        response = requests.get(EVENT_SERVICE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch events")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Event Service: {str(e)}")
    

class DeductBalanceRequest(BaseModel):
    amount: float  # Ensure only `amount` is required in the body

@app.post("/users/{user_id}/deduct_balance")
def deduct_balance(user_id: int, request: DeductBalanceRequest, db: Session = Depends(get_db)):
    # Fetch the user from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user has enough balance
    if user.balance < request.amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient balance. User balance: {user.balance}"
        )

    # Deduct balance
    user.balance -= request.amount
    db.commit()
    db.refresh(user)

    return {
        "message": "Balance deducted successfully",
        "user_id": user_id,
        "deducted_amount": request.amount,
        "remaining_balance": user.balance
    }



BOOKING_SERVICE_URL = "http://127.0.0.1:5000/booking"

@router.post("/user/book_event")
def book_event(data: dict):
    try:
        response = requests.post(BOOKING_SERVICE_URL, json=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Booking failed")
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Booking Service: {str(e)}")


@router.get("/users/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "email": user.email, "balance": user.balance}
