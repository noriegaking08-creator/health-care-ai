# templates/report_writing_template.py
def get_report_writing_prompt(full_conversation: str, diagnosis: str):
    """Template for generating a structured medical report based on the chat."""
    return f"Draft a concise medical summary/report for a primary care physician based on this conversation: '{full_conversation}'. Key points must include initial diagnosis ({diagnosis}) and care plan."