import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

def get_ai_response(user_message: str, user_context: dict = None):
    """
    Get response from AI doctor using OpenAI API or a fallback system
    """
    # Try OpenAI API first (if available)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if openai_api_key:
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}"
            }
            
            # Prepare the prompt with medical context
            system_prompt = f"""
            You are Dr. Alistair Finch, a 50-year experienced, highly professional and empathetic medical doctor.
            You are operating in {user_context.get('location', 'Malawi')} and have specialized knowledge of common diseases, 
            public health campaigns, and local resources in this region.
            
            Provide helpful medical advice that is safe and appropriate. Always recommend seeing a healthcare 
            professional for serious conditions. Never provide prescriptions but offer general guidance.
            """
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
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