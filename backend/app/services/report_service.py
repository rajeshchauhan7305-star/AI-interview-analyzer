from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path
from app.core.config import settings


def generate_pdf_report(report_path: str, interview_data: dict) -> None:
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, height - 60, "AI Interview Analyzer Report")
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 90, f"Candidate: {interview_data.get('user_name', 'N/A')}")
    c.drawString(40, height - 110, f"Category: {interview_data.get('category', 'N/A')}")
    c.drawString(40, height - 130, f"Difficulty: {interview_data.get('difficulty', 'N/A')}")
    c.drawString(40, height - 150, f"Overall Score: {interview_data.get('overall_score', 0)}")
    c.drawString(40, height - 170, f"Recommendation: {interview_data.get('recommendation', 'N/A')}")
    c.drawString(40, height - 200, "Summary:")
    y = height - 220
    for line in interview_data.get("summary", "").splitlines():
        c.drawString(40, y, line)
        y -= 18
        if y < 80:
            c.showPage()
            y = height - 60
    c.save()
