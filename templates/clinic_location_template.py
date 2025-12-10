# templates/clinic_location_template.py
def get_clinic_finder_prompt(location: str):
    """Template for asking the LLM to search for nearby clinics."""
    return f"The patient is in {location}. Search the local database (or use general knowledge) to find and list the three nearest reputable health facilities or clinics."



