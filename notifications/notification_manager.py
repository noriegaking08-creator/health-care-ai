# notification_manager/notification_manager.py
from sqlalchemy.orm import Session
from database.database_manager import Notification
from datetime import datetime, timedelta

def create_notification(db: Session, user_id: int, message: str, type: str):
    """Creates a new notification record in the database."""
    new_notification = Notification(
        user_id=user_id,
        message=message,
        type=type
    )
    db.add(new_notification)
    db.commit()
    return new_notification

def get_unread_notifications(db: Session, user_id: int):
    """Retrieves all unread notifications for a user."""
    notifications = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).order_by(Notification.timestamp.desc()).all()
    return notifications

def schedule_medication_reminder(db: Session, user_id: int, medication: str, time_delay_hours: int):
    """Simulates scheduling a future reminder."""
    reminder_time = datetime.now() + timedelta(hours=time_delay_hours)
    message = f"Time to take your medication, {medication}. Please ensure you follow the doctor's instructions."
    
    # In a real app, this would use a background scheduler (like Celery/RQ)
    print(f"Reminder scheduled for {user_id} at {reminder_time.strftime('%H:%M')}: {message}")
    create_notification(db, user_id, message, 'medication_reminder')