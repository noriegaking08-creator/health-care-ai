
# templates/progress_tracking_template.py
def get_progress_tracking_prompt(history_summary: str, current_symptom: str):
    """Template for tracking sickness/healing progress."""
    return f"Review the following brief conversation history: '{history_summary}'. Based on this, assess the patient's sickness or healing progress regarding '{current_symptom}'. Should the advice escalate (hospital) or continue (home care)? Respond ONLY with a suggestion for the doctor."
