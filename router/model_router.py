# router/model_router.py
from sqlalchemy.orm import Session
from database.database_manager import User
from memory.conversation import get_conversation_history, save_new_message
from templates.system_template import get_doctor_persona_prompt
from model.llm import get_llm_response
from data.data_manager import identify_disease_and_advice
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: int
    message: str

def route_and_respond(db: Session, request: ChatRequest):
    """
    Main function to process a user's message, get an LLM response,
    and manage conversation history.
    """
    user_id = request.user_id
    user_message = request.message
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"response": "User not found. Please log in again."}
        
    user_profile = {
        "full_name": user.full_name,
        "age": user.age,
        "location": user.location
    }
    
    history = get_conversation_history(db, user_id)
    
    # Pre-processing: Check static data for common symptoms
    symptoms = user_message.lower().split() 
    disease_data = identify_disease_and_advice(symptoms)
    
    # Save User Message
    save_new_message(db, user_id, 'user', user_message)
    
    # Construct System Prompt
    system_prompt = get_doctor_persona_prompt(user_profile)
    
    # Integrate static advice (Tool Use Simulation)
    if disease_data:
        initial_advice_tool = (
            f"\n\n[TOOL RESULT: DISEASE IDENTIFICATION]\n"
            f"Likely disease in Malawi: {disease_data['name']}.\n"
            f"Initial Advice: {disease_data['initial_advice']}\n"
            f"INSTRUCTION: Incorporate this advice smoothly into your British English response, maintaining the doctor persona."
        )
        system_prompt += initial_advice_tool

    # Get LLM Response
    llm_response_text = get_llm_response(system_prompt, history + [{"role": "user", "content": user_message}])
    
    # Save Doctor Message
    save_new_message(db, user_id, 'doctor', llm_response_text)
    
    return {"response": llm_response_text}