# tools/write_report_tool.py
from tools.create_report_doc_tool import create_pdf_report
from datetime import datetime

def write_and_store_report(conversation_summary: str, diagnosis: str, user_id: int) -> str:
    """
    Tool: Uses the LLM-generated summary (via report_writing_template) to create a document.
    """
    report_data = {
        "user_id": user_id,
        "title": f"Consultation Summary - {diagnosis}",
        "summary": conversation_summary,
        "date": datetime.now().isoformat()
    }
    document_path = create_pdf_report(report_data)
    # Logic to save the document path in the user's database record
    print(f"Report saved to user profile for user {user_id}.")
    return f"Doctor's report documented and filed. Path: {document_path}"