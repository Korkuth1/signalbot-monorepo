import smtplib
from email.message import EmailMessage
import os

def send_email(subject: str, body: str):
    EMAIL_ADDRESS = os.getenv("BOT_EMAIL")
    EMAIL_PASSWORD = os.getenv("BOT_PASS")
    TO_EMAIL = os.getenv("TARGET_EMAIL")

    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL]):
        print("Email credentials not set.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.mail.me.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email sent.")
    except Exception as e:
        print(f"Email error: {e}")

send_email("SignalBot Update", "Dies ist eine Test-E-Mail vom SignalBot!")
