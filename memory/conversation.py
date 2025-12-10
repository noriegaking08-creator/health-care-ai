# memory/conversation.py
from sqlalchemy.orm import Session
from database.database_manager import Conversation, Message

def get_conversation_history(db: Session, user_id: int):
    """Retrieves all messages for the active conversation of a user."""
    conversation = db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.timestamp.desc()).first()
    
    if not conversation:
        return []

    messages = db.query(Message).filter(Message.conversation_id == conversation.id).order_by(Message.timestamp).all()
    
    # Format for LLM: [{"role": "user/assistant", "content": "..."}]
    history = []
    for msg in messages:
        role = 'assistant' if msg.sender == 'doctor' else 'user'
        history.append({"role": role, "content": msg.content})
        
    return history

def save_new_message(db: Session, user_id: int, sender: str, content: str):
    """Saves a new message and ensures an active conversation exists."""
    conversation = db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.timestamp.desc()).first()
    
    # Create a new conversation if none exists
    if not conversation:
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save the new message
    new_message = Message(
        conversation_id=conversation.id,
        sender=sender, # 'user' or 'doctor'
        content=content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return new_message