import json
import sqlite3
import os
import bcrypt
from urllib.parse import parse_qs
from datetime import datetime
import requests

# Database functions for Vercel compatibility
def get_db_connection():
    # Use a temporary location that works with Vercel's ephemeral filesystem
    db_path = '/tmp/healthcom.db' 
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT,
            age INTEGER,
            location TEXT DEFAULT 'Malawi',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_user_by_username(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return dict(user) if user else None

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user['hashed_password']):
        return None
    return user

def create_user(user_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user already exists
    existing_user = get_user_by_username(user_data['username'])
    if existing_user:
        conn.close()
        return {"error": "Username already registered"}
    
    # Create new user
    hashed_password = get_password_hash(user_data['password'])
    cursor.execute('''
        INSERT INTO users (username, hashed_password, full_name, age, location)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        user_data['username'],
        hashed_password,
        user_data.get('full_name'),
        user_data.get('age'),
        user_data.get('location', 'Malawi')
    ))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "user_id": user_id,
        "username": user_data['username'],
        "message": "User registered successfully"
    }

def get_user_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return {"error": "User not found"}
    
    user_dict = dict(user)
    # Remove sensitive data
    del user_dict['hashed_password']
    return user_dict

# AI Doctor functionality
def get_ai_response(user_message: str, user_context: dict = None):
    """
    Get response from AI doctor using Hugging Face Inference API or a fallback system
    """
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

# Vercel-compatible handler function
def handle_request(event, context):
    # Parse HTTP method and path
    method = event['httpMethod']
    path = event['path']
    
    # Parse query parameters
    query_params = parse_qs(event.get('queryStringParameters', {}) or {})
    
    # Parse request body
    body = event.get('body')
    if body:
        try:
            body_data = json.loads(body)
        except:
            body_data = {}
    else:
        body_data = {}
    
    # Handle API routes
    if path == '/api/users/register' and method == 'POST':
        result = create_user(body_data)
        if "error" in result:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"detail": result["error"]})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
    
    elif path == '/api/users/login' and method == 'POST':
        user = authenticate_user(body_data.get('username'), body_data.get('password'))
        if not user:
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"detail": "Invalid credentials"})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "user_id": user['id'],
                "username": user['username'],
                "message": "Login successful"
            })
        }
    
    elif path.startswith('/api/users/') and method == 'GET':
        # Extract user_id from path
        user_id = int(path.split('/')[-1])
        user = get_user_profile(user_id)
        
        if "error" in user:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"detail": user["error"]})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(user)
        }
    
    elif path == '/api/chat/message' and method == 'POST':
        user_id = body_data.get('user_id')
        message = body_data.get('message')
        
        user = get_user_profile(user_id)
        if "error" in user:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"detail": user["error"]})
            }
        
        user_context = {
            "full_name": user.get('full_name', 'Patient'),
            "age": user.get('age'),
            "location": user.get('location', 'Malawi')
        }
        
        ai_response = get_ai_response(message, user_context)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"response": ai_response})
        }
    
    elif path == '/api/health' and method == 'GET':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"status": "healthy", "message": "HealthCom API is running"})
        }
    
    # Default response for unknown paths
    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({"error": "Endpoint not found"})
    }

# Make the handler accessible
handler = handle_request