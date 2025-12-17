from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import bcrypt
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional
import sys
import importlib.util

# Load environment variables
load_dotenv()

# Add backend directory to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import required models and functions from backend directory
# We'll define them inline since we're consolidating

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./healthco.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define models and functions inline since we're consolidating everything
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional
from datetime import datetime

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    age = Column(Integer)
    location = Column(String, default="Malawi")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    messages = relationship("Message", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="Health Consultation")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who sent the message
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")

# Pydantic Models for API
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = "Malawi"

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    age: Optional[int]
    location: Optional[str]

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    user_id: int
    username: str
    message: str

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    response: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True

# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Auth functions
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user_data: UserCreate):
    # Check if user already exists
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        age=user_data.age,
        location=user_data.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# AI Doctor functionality
import requests

def get_ai_response(user_message: str, user_context: dict = None):
    """
    Get response from AI doctor using Hugging Face Inference API or a fallback system
    """
    # Try Hugging Face API first (if available)
    hf_api_key = os.getenv("HF_API_KEY")

    if hf_api_key:
        try:
            headers = {
                "Authorization": f"Bearer {hf_api_key}",
                "Content-Type": "application/json"
            }

            # Prepare the prompt with medical context for Medalpaca
            system_prompt = f"""
            Below is a medical consultation scenario. Provide a detailed and helpful response based on the user's health concerns.

            Context: You are speaking with a patient from {user_context.get('location', 'Malawi')}.
            Patient details: {user_context.get('full_name', 'Patient')}, age {user_context.get('age', 'unknown')} years old.

            Question: {user_message}

            Answer: As a medical professional, provide helpful medical advice that is safe and appropriate. Always recommend seeing a healthcare professional for serious conditions. Never provide prescriptions but offer general guidance.
            """

            # For Medalpaca-7b, we use the text generation endpoint
            data = {
                "inputs": system_prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                },
                "options": {
                    "wait_for_model": True
                }
            }

            response = requests.post(
                "https://api-inference.huggingface.co/models/medalpaca/medalpaca-7b",
                headers=headers,
                json=data,
                timeout=60  # Longer timeout for Hugging Face API
            )

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    # Extract only the answer part after the question
                    if "Answer:" in generated_text:
                        answer = generated_text.split("Answer:")[-1].strip()
                        return answer
                    return generated_text.strip()
                return result.get("generated_text", "").strip()

        except Exception as e:
            print(f"Hugging Face API error: {e}")
            # Fall through to fallback system

    # Fallback system
    return get_fallback_response(user_message, user_context)

def get_fallback_response(user_message: str, user_context: dict = None):
    """
    Fallback medical advice system when API is not available
    """
    user_lower = user_message.lower()

    # Common symptom-based responses
    if any(symptom in user_lower for symptom in ["fever", "temperature", "hot", "cold", "chills", "sweat"]):
        return ("Based on your reported symptoms, it sounds like you may have a fever. "
                "I recommend staying hydrated, resting, and monitoring your temperature. "
                "If your fever is high (above 38.5°C/101.3°F) or persists for more than 2 days, "
                "please seek medical attention at a local clinic.")

    elif any(symptom in user_lower for symptom in ["headache", "pain", "hurt", "ach", "sore"]):
        return ("For headaches, I recommend resting in a quiet, dark room and staying hydrated. "
                "Over-the-counter pain relievers like paracetamol can help, but follow package instructions. "
                "If the headache is severe, persistent, or accompanied by other serious symptoms, "
                "please see a healthcare professional.")

    elif any(symptom in user_lower for symptom in ["stomach", "belly", "nausea", "vomit", "diarrhea", "loose motion"]):
        return ("For stomach issues, stay hydrated with clean water or oral rehydration solutions. "
                "Eat light, plain foods like rice, toast, or bananas. Avoid fatty, spicy, or dairy foods. "
                "If vomiting or diarrhea persists for more than 24 hours or you show signs of dehydration, "
                "seek immediate medical care.")

    elif any(symptom in user_lower for symptom in ["cough", "cold", "sneeze", "sore throat", "throat"]):
        return ("For coughs and colds, rest well and drink plenty of fluids. "
                "Gargling with warm salt water can soothe a sore throat. "
                "If you have difficulty breathing, chest pain, or symptoms worsen, "
                "please consult with a healthcare provider.")

    elif any(word in user_lower for word in ["hello", "hi", "good morning", "good afternoon", "good evening"]):
        location = user_context.get('location', 'Malawi') if user_context else 'Malawi'
        return (f"Hello! I'm Dr. Alistair Finch. How are you feeling today? Please describe any symptoms or concerns you have, "
                f"and I'll do my best to provide helpful guidance. I understand you're in {location}.")

    elif any(word in user_lower for word in ["thank", "thanks", "appreciate"]):
        return ("You're welcome! I'm here to help. If you have any other questions or concerns, please feel free to ask.")

    elif any(word in user_lower for word in ["help", "assist", "problem", "issue"]):
        return ("I'm here to help. Please describe your symptoms or health concern in detail. "
                "I can provide general health guidance, but remember that I'm not a substitute "
                "for proper medical diagnosis and treatment. For serious conditions, please seek professional care.")

    else:
        # General fallback responses
        return ("Thank you for sharing your health concern. I recommend consulting with a healthcare professional "
                "for proper evaluation and treatment. I can provide general health guidance, but remember that "
                "I'm not a substitute for proper medical diagnosis and treatment. "
                "For serious conditions, please seek professional care immediately.")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HealthCom API",
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

# API Endpoints
@app.post("/api/users/register", response_model=LoginResponse)
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

@app.post("/api/users/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginResponse(
        user_id=user.id,
        username=user.username,
        message="Login successful"
    )

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_profile(db, user_id)
    return user

@app.post("/api/chat/message", response_model=ChatResponse)
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

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "HealthCom API is running"}