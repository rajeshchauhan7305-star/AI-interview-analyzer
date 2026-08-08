import smtplib
from email.message import EmailMessage
from app.core.config import settings


def send_email(subject: str, recipient: str, html_body: str, text_body: str | None = None) -> bool:
    text_body = text_body or html_body
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.EMAIL_FROM
    message["To"] = recipient
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    if not settings.SMTP_SERVER or not settings.SMTP_PORT:
        print("SMTP not configured, skipping email send")
        print(f"Email content for {recipient}: {subject}\n{text_body}")
        return False

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10) as smtp:
            smtp.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(message)
        return True
    except Exception as exc:
        print(f"Failed to send email to {recipient}: {exc}")
        return False
