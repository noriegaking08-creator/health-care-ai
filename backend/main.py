from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import bcrypt
import os
from dotenv import load_dotenv
from models import Base, User, Conversation, Message, UserCreate, UserResponse, LoginRequest, LoginResponse, ChatRequest, ChatResponse
from datetime import datetime
from typing import Optional
import requests

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./healthco.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HealthCo API",
    description="A healthcare application backend with AI doctor functionality",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Import authentication functions
from auth import authenticate_user, create_user, get_user_profile
from ai_doctor import get_ai_response

# API Endpoints
@app.post("/users/register", response_model=LoginResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user_data)
        return LoginResponse(
            user_id=db_user.id,
            username=db_user.username,
            message="User registered successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/users/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginResponse(
        user_id=user.id,
        username=user.username,
        message="Login successful"
    )

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_profile(db, user_id)
    return user

@app.post("/chat/message", response_model=ChatResponse)
def chat_with_doctor(chat_data: ChatRequest, db: Session = Depends(get_db)):
    # Get the user to provide context
    user = get_user_profile(db, chat_data.user_id)
    user_context = {
        "full_name": user.full_name,
        "age": user.age,
        "location": user.location
    }

    # Get AI response
    ai_response = get_ai_response(chat_data.message, user_context)

    # Create conversation and save message (optional, for history)
    # For this implementation, we'll just return the AI response
    return ChatResponse(response=ai_response)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "HealthCo API is running"}