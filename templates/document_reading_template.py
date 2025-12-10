# templates/document_reading_template.py
def get_document_reading_prompt(document_summary: str):
    """Template for analyzing uploaded medical documents."""
    return f"A medical document summary has been uploaded: '{document_summary}'. Analyze this summary and formulate professional, supportive questions for the patient based on these findings."