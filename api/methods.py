# api/methods.py
# Utility functions used across API endpoints (e.g., JWT token creation, input validation)
import bcrypt

def hash_password(password: str) -> str:
    """Secure password hashing using bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifying hashed passwords using bcrypt."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))