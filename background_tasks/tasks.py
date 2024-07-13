import os
from celery import Celery
from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

celery = Celery("tasks", broker="pyamqp://")

@celery.task
def send_mail(email_address):
    port = 587
    smtp_server = "live.smtp.mailtrap.io"
    login = os.getenv("MAILTRAP_USER")
    password = os.getenv("MAILTRAP_PASSWORD")

    sender_email = "mailtrap@osinachi.me"
    receiver_email = email_address

    text = """\
    Hi,
    This is a test message from this automation app. Feel free to use. Thanks!
    """

    message = MIMEText(text, "plain")
    message["Subject"] = "Email from flask automation app!"
    message["From"] = sender_email
    message["To"] = receiver_email

    with SMTP(smtp_server, port) as server:
        try:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        except SMTPException as e:
            print(f"Failed to send email: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    return "Email sent successfully"