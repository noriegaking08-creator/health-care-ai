import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

def get_ai_response(user_message: str, user_context: dict = None):
    """
    Get response from AI doctor using Hugging Face API or a fallback system
    """
    # Try Hugging Face API first (if available)
    hf_api_key = os.getenv("HF_API_KEY")

    if hf_api_key:
        try:
            headers = {
                "Authorization": f"Bearer {hf_api_key}",
                "Content-Type": "application/json"
            }

            # Prepare the prompt with medical context for Medical-specific model
            system_prompt = f"""
            Below is a medical consultation scenario. Provide a detailed and helpful response based on the user's health concerns.

            Context: You are speaking with a patient from {user_context.get('location', 'Malawi')}.
            Patient details: {user_context.get('full_name', 'Patient')}, age {user_context.get('age', 'unknown')} years old.

            Question: {user_message}

            Answer: As a medical professional, provide helpful medical advice that is safe and appropriate. Always recommend seeing a healthcare professional for serious conditions. Never provide prescriptions but offer general guidance.
            """

            # Using a medical-specific model from Hugging Face
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

            # Using a medical domain-specific model
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
    Comprehensive fallback medical advice system when API is not available
    """
    user_lower = user_message.lower()

    # Common symptom-based responses
    if any(symptom in user_lower for symptom in ["fever", "temperature", "hot", "cold", "chills", "sweat", "feeling hot", "feeling cold"]):
        return ("Based on your reported symptoms, it sounds like you may have a fever. "
                "I recommend staying hydrated, resting, and monitoring your temperature. "
                "Apply cool, damp cloths to your forehead and take lukewarm baths to help reduce fever. "
                "If your fever is high (above 38.5°C/101.3°F), persists for more than 2 days, "
                "or is accompanied by severe symptoms like difficulty breathing, persistent vomiting, or confusion, "
                "please seek immediate medical attention at a local clinic.")

    elif any(symptom in user_lower for symptom in ["headache", "pain", "hurt", "ach", "sore", "throbbing", "pounding"]):
        return ("For headaches, I recommend resting in a quiet, dark room and staying hydrated. "
                "Apply a cold or warm compress to your forehead or neck depending on what feels better. "
                "Over-the-counter pain relievers like paracetamol can help, but follow package instructions. "
                "Avoid bright lights, loud noises, and strong smells. "
                "If the headache is severe, sudden, accompanied by fever, stiff neck, rash, or vision changes, "
                "or if it's the worst headache you've ever experienced, please see a healthcare professional immediately.")

    elif any(symptom in user_lower for symptom in ["stomach", "belly", "nausea", "vomit", "diarrhea", "loose motion", "upset stomach", "stomach ache"]):
        return ("For stomach issues, stay hydrated with clean water, oral rehydration solutions, or clear broths. "
                "Follow the BRAT diet (bananas, rice, applesauce, toast) initially, then gradually return to normal foods. "
                "Eat small, frequent meals instead of large ones. Avoid fatty, spicy, dairy, caffeine, and alcohol. "
                "Rest and avoid solid foods for a few hours if vomiting occurs, then slowly reintroduce clear liquids. "
                "If vomiting or diarrhea persists for more than 24 hours, you show signs of dehydration (dry mouth, dizziness, little urination), "
                "or you experience severe abdominal pain, blood in vomit/stool, or high fever, seek immediate medical care.")

    elif any(symptom in user_lower for symptom in ["cough", "cold", "sneeze", "sore throat", "throat", "runny nose", "stuffy nose"]):
        return ("For coughs and colds, rest well and drink plenty of fluids like water, herbal teas, or clear broths. "
                "Gargle with warm salt water to soothe a sore throat. Use a humidifier or take steamy showers to ease congestion. "
                "Honey in warm water or tea can help soothe coughs (not for children under 1 year). "
                "Over-the-counter cough drops or pain relievers may provide relief. "
                "If you have difficulty breathing, chest pain, persistent fever above 38.5°C/101.3°F, "
                "cough lasting more than 2 weeks, or symptoms worsen, please consult with a healthcare provider.")

    elif any(symptom in user_lower for symptom in ["chest pain", "chest tightness", "difficulty breathing", "short of breath", "wheezing", "breathing problem"]):
        return ("Chest pain and breathing difficulties can be serious symptoms requiring immediate medical attention. "
                "If you're experiencing severe chest pain, especially if it radiates to your arm, neck, or jaw, "
                "or if you have severe difficulty breathing, dizziness, or sudden onset of these symptoms, "
                "seek emergency medical care immediately. For milder symptoms, monitor closely and see a healthcare provider "
                "as soon as possible to determine the cause, which could range from heart issues to respiratory problems.")

    elif any(symptom in user_lower for symptom in ["rash", "itchy", "skin", "red spots", "hives", "bumps", "swelling"]):
        return ("For skin rashes, avoid scratching and keep the area clean and dry. "
                "Apply cool compresses or calamine lotion to soothe itching. "
                "Take antihistamines if appropriate and not contraindicated by other conditions. "
                "Avoid known irritants and allergens. "
                "If the rash spreads rapidly, is accompanied by fever, breathing difficulties, "
                "or if it appears infected (pus, warmth, red streaking), seek medical attention immediately. "
                "Also see a healthcare provider if the rash doesn't improve after a few days of home care.")

    elif any(symptom in user_lower for symptom in ["joint pain", "joint ache", "arthritis", "stiff joints", "swollen joints", "muscle pain"]):
        return ("For joint or muscle pain, rest the affected area and apply ice for the first 48 hours to reduce swelling, "
                "then use heat to relax muscles and improve blood flow. "
                "Gentle stretching and movement can help maintain flexibility. "
                "Over-the-counter pain relievers like ibuprofen or paracetamol may help, following package instructions. "
                "Maintain a healthy weight to reduce stress on joints. "
                "If pain persists for more than a week, is severe, accompanied by swelling, redness, warmth, "
                "or if you have difficulty moving the joint, consult a healthcare provider.")

    elif any(symptom in user_lower for symptom in ["dizziness", "lightheaded", "faint", "spinning", "balance", "vertigo"]):
        return ("For dizziness, sit or lie down immediately to prevent falls. "
                "Stay hydrated and get up slowly from sitting or lying positions. "
                "Avoid sudden head movements and bright lights. "
                "If dizziness is accompanied by chest pain, difficulty breathing, severe headache, "
                "numbness, weakness, or difficulty speaking, seek emergency care immediately. "
                "For persistent or recurring dizziness, see a healthcare provider to determine the cause.")

    elif any(symptom in user_lower for symptom in ["abdominal pain", "stomach ache", "belly pain", "cramps", "stomach cramps"]):
        return ("For abdominal pain, try to identify any triggers like food, stress, or activity. "
                "Apply a warm compress to the area for relief. "
                "Stay hydrated and eat small, bland meals. Avoid foods that worsen the pain. "
                "If pain is severe, localized to one area, accompanied by fever, vomiting, blood in stool, "
                "or if pain came on suddenly and is very intense, seek immediate medical attention. "
                "Also see a healthcare provider if pain persists for more than 24 hours or keeps recurring.")

    elif any(symptom in user_lower for symptom in ["fatigue", "tired", "exhausted", "weak", "low energy", "sleepy"]):
        return ("For fatigue, ensure you're getting adequate sleep (7-9 hours for most adults), "
                "eating a balanced diet, and staying hydrated. "
                "Regular, moderate exercise can actually help reduce fatigue. "
                "Manage stress through relaxation techniques. "
                "If fatigue persists despite adequate rest, is severe, or is accompanied by other symptoms "
                "like unexplained weight loss, fever, or weakness, consult a healthcare provider "
                "as it could indicate an underlying condition.")

    elif any(symptom in user_lower for symptom in ["back pain", "lower back", "upper back", "spine pain", "back ache"]):
        return ("For back pain, apply heat or ice to the affected area for 15-20 minutes several times a day. "
                "Maintain good posture and avoid heavy lifting. "
                "Gentle stretching and walking may help. "
                "Over-the-counter pain relievers can provide temporary relief. "
                "Sleep with a pillow between your knees (if lying on your side) or under your knees (if on your back). "
                "If pain is severe, persists for more than a week, is accompanied by numbness or weakness in legs, "
                "or if you have difficulty controlling bladder or bowels, seek immediate medical attention.")

    elif any(symptom in user_lower for symptom in ["sleep", "insomnia", "can't sleep", "trouble sleeping", "sleeping problem"]):
        return ("For sleep problems, maintain a regular sleep schedule and create a comfortable sleep environment. "
                "Avoid caffeine, large meals, and screens at least 2 hours before bedtime. "
                "Try relaxation techniques like deep breathing or meditation. "
                "Keep the bedroom cool, dark, and quiet. "
                "If sleep problems persist for more than 2-3 weeks, significantly impact your daily life, "
                "or are accompanied by other concerning symptoms, consult a healthcare provider.")

    elif any(word in user_lower for word in ["hello", "hi", "good morning", "good afternoon", "good evening", "greetings"]):
        location = user_context.get('location', 'Malawi') if user_context else 'Malawi'
        return (f"Hello! I'm Dr. Alistair Finch. How are you feeling today? Please describe any symptoms or concerns you have, "
                f"and I'll do my best to provide helpful guidance. I understand you're in {location}. "
                "Remember, I can provide general health guidance, but for serious conditions, "
                "please seek professional medical care.")

    elif any(word in user_lower for word in ["thank", "thanks", "appreciate", "grateful", "appreciated"]):
        return ("You're very welcome! I'm here to help. If you have any other questions or concerns, please feel free to ask. "
                "Remember to consult with healthcare professionals for serious conditions or persistent symptoms.")

    elif any(word in user_lower for word in ["help", "assist", "problem", "issue", "concern", "worried"]):
        return ("I'm here to help. Please describe your symptoms or health concern in detail. "
                "I can provide general health guidance, but remember that I'm not a substitute "
                "for proper medical diagnosis and treatment. For serious conditions, persistent symptoms, "
                "or if you're experiencing severe pain, difficulty breathing, chest pain, or other emergency symptoms, "
                "please seek immediate professional medical care.")

    elif any(word in user_lower for word in ["medicine", "medication", "prescription", "drug", "treatment"]):
        return ("I cannot provide prescriptions or specific medication advice. "
                "Only licensed healthcare professionals can prescribe medications after proper evaluation. "
                "If you need medication, please consult with a healthcare provider who can assess your condition "
                "and prescribe appropriate treatment. For over-the-counter medications, follow package instructions "
                "and consult a pharmacist if you have questions about interactions or appropriateness for your condition.")

    elif any(word in user_lower for word in ["pregnant", "pregnancy", "expecting", "baby", "conceiving"]):
        return ("Pregnancy-related health concerns require specialized medical care. "
                "If you're pregnant or suspect you might be, please consult with an obstetrician or healthcare provider "
                "who can provide appropriate prenatal care. Avoid taking any medications without medical approval, "
                "maintain a healthy diet, take prenatal vitamins, and avoid harmful substances like alcohol and tobacco. "
                "Seek immediate medical attention for severe symptoms like heavy bleeding, severe abdominal pain, "
                "or signs of preterm labor.")

    elif any(word in user_lower for word in ["child", "children", "kid", "infant", "baby", "pediatric"]):
        return ("Children have different health needs and medication dosages than adults. "
                "For pediatric concerns, please consult with a pediatrician or healthcare provider "
                "who specializes in children's health. Some symptoms that might be minor in adults "
                "can be serious in children. Seek immediate medical attention for infants under 3 months "
                "with fever, persistent crying, difficulty breathing, or feeding problems.")

    elif any(word in user_lower for word in ["elderly", "old", "aging", "senior", "aged"]):
        return ("Older adults may have different health considerations and medication sensitivities. "
                "If you're caring for an elderly person or are elderly yourself, be aware that "
                "symptoms might present differently than in younger adults. "
                "Pay special attention to changes in mental status, falls, medication interactions, "
                "and chronic condition management. Regular check-ups with healthcare providers "
                "are important for preventive care and early detection of health issues.")

    elif any(word in user_lower for word in ["emergency", "urgent", "911", "ambulance", "hospital"]):
        return ("If you're experiencing a medical emergency such as severe chest pain, difficulty breathing, "
                "severe bleeding, loss of consciousness, signs of stroke (facial drooping, arm weakness, speech difficulty), "
                "severe allergic reaction, or severe injury, call emergency services immediately (911 or your local emergency number). "
                "Do not delay seeking emergency care while waiting for medical advice. Emergency services can provide "
                "life-saving care during transport to the hospital.")

    elif any(word in user_lower for word in ["allergy", "allergic", "reaction", "anaphylaxis", "hives"]):
        return ("For mild allergic reactions like localized hives or itching, antihistamines may help. "
                "Avoid the known allergen if possible. For severe allergic reactions (difficulty breathing, "
                "swelling of face/throat, rapid pulse, dizziness), this is a medical emergency. "
                "Use an epinephrine auto-injector if available and call emergency services immediately. "
                "Always carry prescribed epinephrine if you have known severe allergies.")

    elif any(word in user_lower for word in ["diabetes", "blood sugar", "insulin", "glucose"]):
        return ("Diabetes management requires careful monitoring and medical supervision. "
                "If you have diabetes, monitor your blood sugar as directed by your healthcare provider. "
                "Take medications as prescribed and maintain a consistent eating schedule. "
                "If you experience symptoms of low blood sugar (shakiness, sweating, confusion) "
                "consume fast-acting carbohydrates. For high blood sugar symptoms (excessive thirst, "
                "frequent urination, fatigue), stay hydrated and contact your healthcare provider. "
                "Seek immediate medical attention for severe symptoms like difficulty breathing, "
                "fruity-smelling breath, or altered consciousness.")

    elif any(word in user_lower for word in ["heart", "cardiac", "blood pressure", "hypertension", "cardiovascular"]):
        return ("Heart health is crucial. If you have known heart conditions, take medications as prescribed "
                "and follow your healthcare provider's recommendations. For symptoms like chest pain, "
                "shortness of breath, irregular heartbeat, or severe fatigue, seek immediate medical attention. "
                "Maintain a heart-healthy lifestyle with regular exercise, a balanced diet low in sodium and saturated fats, "
                "and stress management. Monitor blood pressure as recommended by your healthcare provider.")

    elif any(word in user_lower for word in ["mental health", "depression", "anxiety", "stress", "suicide", "mental"]):
        return ("Mental health is as important as physical health. If you're experiencing persistent sadness, "
                "anxiety, overwhelming stress, or thoughts of self-harm, please reach out to mental health professionals, "
                "counselors, or crisis helplines immediately. Many communities have mental health resources and hotlines. "
                "Don't hesitate to seek help - mental health conditions are treatable. "
                "If you're having thoughts of self-harm, please contact emergency services or a crisis hotline immediately.")

    else:
        # General fallback responses
        return ("Thank you for sharing your health concern. I recommend consulting with a healthcare professional "
                "for proper evaluation and treatment. I can provide general health guidance, but remember that "
                "I'm not a substitute for proper medical diagnosis and treatment. "
                "For serious conditions, persistent symptoms, or if you're experiencing severe pain, "
                "difficulty breathing, chest pain, or other emergency symptoms, please seek professional care immediately. "
                "Always follow up with qualified healthcare providers who can examine you and provide personalized treatment plans.")