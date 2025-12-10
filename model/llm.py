# model/llm.py
import os
import requests
import random
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'utilities', 'secret', '.env'))

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
ZHIPU_API_URL = "https://api.zhipu.ai/v1/chat/completions" # Placeholder URL

def get_llm_response(system_prompt: str, conversation_history: list):
    """Generates a response from the ZhiPu LLM with fallback to rule-based responses."""
    if not ZHIPU_API_KEY:
        # Fallback to rule-based system if API key is not set
        return get_fallback_response(conversation_history[-1]['content'] if conversation_history else "Hello")

    messages = [{"role": "system", "content": system_prompt}] + conversation_history

    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "glm-4", # Example model
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(ZHIPU_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()

        data = response.json()
        return data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        print(f"ZHIPU API Request Error: {e}")
        # Fallback to rule-based system
        return get_fallback_response(conversation_history[-1]['content'] if conversation_history else "Hello")
    except KeyError:
        print("ZHIPU API Response Error: Malformed response")
        # Fallback to rule-based system
        return get_fallback_response(conversation_history[-1]['content'] if conversation_history else "Hello")


def get_fallback_response(user_message: str):
    """Provides rule-based responses when the LLM API is unavailable."""
    user_message_lower = user_message.lower()

    # Common symptom-based responses
    if any(symptom in user_message_lower for symptom in ["fever", "temperature", "hot", "cold", "chills", "sweat"]):
        return ("Based on your reported symptoms, it sounds like you may have a fever. "
                "I recommend staying hydrated, resting, and monitoring your temperature. "
                "If your fever is high (above 38.5°C/101.3°F) or persists for more than 2 days, "
                "please seek medical attention at a local clinic.")

    elif any(symptom in user_message_lower for symptom in ["headache", "pain", "hurt", "ach", "sore"]):
        return ("For headaches, I recommend resting in a quiet, dark room and staying hydrated. "
                "Over-the-counter pain relievers like paracetamol can help, but follow package instructions. "
                "If the headache is severe, persistent, or accompanied by other serious symptoms, "
                "please see a healthcare professional.")

    elif any(symptom in user_message_lower for symptom in ["stomach", "belly", "nausea", "vomit", "diarrhea", "loose motion"]):
        return ("For stomach issues, stay hydrated with clean water or oral rehydration solutions. "
                "Eat light, plain foods like rice, toast, or bananas. Avoid fatty, spicy, or dairy foods. "
                "If vomiting or diarrhea persists for more than 24 hours or you show signs of dehydration, "
                "seek immediate medical care.")

    elif any(symptom in user_message_lower for symptom in ["cough", "cold", "sneeze", "sore throat", "throat"]):
        return ("For coughs and colds, rest well and drink plenty of fluids. "
                "Gargling with warm salt water can soothe a sore throat. "
                "If you have difficulty breathing, chest pain, or symptoms worsen, "
                "please consult with a healthcare provider.")

    elif any(word in user_message_lower for word in ["hello", "hi", "good morning", "good afternoon", "good evening"]):
        return ("Hello! I'm Dr. Alistair Finch. How are you feeling today? Please describe any symptoms or concerns you have, and I'll do my best to provide helpful guidance.")

    elif any(word in user_message_lower for word in ["thank", "thanks", "appreciate"]):
        return ("You're welcome! I'm here to help. If you have any other questions or concerns, please feel free to ask.")

    elif any(word in user_message_lower for word in ["help", "assist", "problem", "issue"]):
        return ("I'm here to help. Please describe your symptoms or health concern in detail. "
                "I can provide general health guidance, but remember that I'm not a substitute "
                "for proper medical diagnosis and treatment. For serious conditions, please seek professional care.")

    else:
        # General fallback responses
        general_responses = [
            f"I understand you're concerned about '{user_message[:50]}...'. Based on the information provided, I recommend consulting with a healthcare professional for proper evaluation and treatment.",
            f"Thank you for sharing your concern about '{user_message[:50]}...'. It's important to get proper medical evaluation for accurate diagnosis and treatment.",
            f"I appreciate you sharing your health concern: '{user_message[:50]}...'. Remember, I can provide general guidance, but for accurate diagnosis and treatment, please see a healthcare professional.",
            f"I've noted your concern about '{user_message[:50]}...'. For the most accurate assessment and appropriate treatment, I recommend seeing a healthcare provider who can properly evaluate your condition."
        ]
        return random.choice(general_responses)