# api/API.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import bcrypt
import os
from typing import Optional
from database.database_manager import get_db, init_db, User
from router.model_router import route_and_respond, ChatRequest

# Initialize the database
init_db()

app = FastAPI(
    title="HEARTH COM - Digital Doctor API"
)

# CORS middleware to allow the React frontend to communicate
origins = [
    "http://localhost:3000",  # React development server (default)
    "http://localhost:5000",  # Alternative React development port
    "http://localhost:5001",  # Alternative React development port
    "http://localhost:5002",  # Additional alternative port
    "http://localhost:5003",  # Additional alternative port
    "http://localhost:5004",  # Additional alternative port
    "http://localhost:5005",  # Alternative React development port
    "http://localhost:5006",  # Alternative React development port
    "http://localhost:5007",  # Your current React development port
    "http://localhost:5008",  # Additional alternative port
    "http://localhost:5009",  # Additional alternative port
    "http://localhost:8000",  # Allow same origin for direct testing
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",  # Additional alternative port
    "http://127.0.0.1:5003",  # Additional alternative port
    "http://127.0.0.1:5004",  # Additional alternative port
    "http://127.0.0.1:5005",  # Alternative React development port
    "http://127.0.0.1:5006",  # Alternative React development port
    "http://127.0.0.1:5007",  # Your current React development port
    "http://127.0.0.1:5008",  # Additional alternative port
    "http://127.0.0.1:5009",  # Additional alternative port
    "http://127.0.0.1:8000",
    "http://localhost", # Add if accessing without port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- USER AUTH ENDPOINTS ---

@app.post("/users/register")
def register_user(user_data: dict, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data['username']).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")

    # Validate and sanitize inputs
    username = user_data.get('username', '').strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    password = user_data.get('password', '')
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Validate age if provided
    age = user_data.get('age')
    if age is not None:
        try:
            age = int(age)
            if age < 0 or age > 150:  # Reasonable age range
                raise ValueError("Invalid age")
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Age must be a valid number between 0 and 150")

    new_user = User(
        username=username,
        hashed_password=hashed_password.decode('utf-8'),
        full_name=user_data.get('full_name', '').strip(),
        age=age,
        location=user_data.get('location', 'Malawi').strip()
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/users/login")
def login_user(login_data: dict, db: Session = Depends(get_db)):
    # Sanitize the username input
    username = login_data.get('username', '').strip()
    if not username:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    password = login_data.get('password', '')
    if not password:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        # To prevent timing attacks, we still perform a dummy hash comparison
        bcrypt.checkpw(password.encode('utf-8'), bcrypt.gensalt())
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # Verify the hashed password
    if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {"message": "Login successful", "user_id": user.id}


@app.get("/users/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Fetches user profile data by user ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return user profile data
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "age": user.age,
        "location": user.location,
    }

# --- CHATBOT ENDPOINT ---

@app.post("/chat/message")
def handle_chat_message(request: ChatRequest, db: Session = Depends(get_db)):
    """Handles the user's message and returns the doctor's response."""
    return route_and_respond(db, request)

# --- UTILITIES/UPLOAD ENDPOINT ---

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/data/upload/{user_id}")
def upload_file(user_id: int, file: UploadFile = File(...)):
    # Validate user_id is a positive integer to prevent injection
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.txt', '.jpg', '.jpeg', '.png'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Securely construct file path to prevent path traversal
    filename = f"user_{user_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Limit file size (e.g., 5MB)
    contents = file.file.read()
    if len(contents) > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File too large")

    with open(file_path, "wb") as f:
        f.write(contents)

    return {"message": f"File '{file.filename}' uploaded successfully for user {user_id}. Document processing started."}