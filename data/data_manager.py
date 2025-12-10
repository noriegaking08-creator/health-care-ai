# data/data_manager.py
import json
import os

def load_disease_data():
    """Loads the disease dataset from the data.json file."""
    # Construct path relative to the current file
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {"diseases": []}

def identify_disease_and_advice(symptoms: list):
    """
    Simulates checking the dataset for a matching disease based on symptoms.
    """
    data = load_disease_data()
    best_match = None
    max_match_count = 0

    # Simple keyword matching logic
    for disease in data.get("diseases", []):
        match_count = sum(1 for symptom in symptoms if symptom.lower() in [s.lower() for s in disease["symptoms"]])
        if match_count > max_match_count:
            max_match_count = match_count
            best_match = disease
    
    if best_match and max_match_count > 0:
        return best_match
    return None