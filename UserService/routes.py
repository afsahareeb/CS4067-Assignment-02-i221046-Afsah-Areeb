import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from pydantic import BaseModel
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def home():
    return {"message": "Welcome to User Service!"}

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or user.password_hash != request.password:  # TODO: Hash password before comparing
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful!"}

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    db_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password_hash=request.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User created successfully!"}

EVENT_SERVICE_URL = "http://127.0.0.1:8000/eventDashboard/"  # URL of event service

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

@router.put("/users/{user_id}/update_balance")
def update_balance(user_id: int, balance: float, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.balance = balance  # ✅ Update balance
    db.commit()
    return {"message": "Balance updated successfully", "new_balance": user.balance}
