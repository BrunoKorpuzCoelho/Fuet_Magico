from celery import shared_task
from time import sleep

@shared_task
def test_celery_task(message):
    print(f"[Celery Test] Starting task with message: {message}")
    sleep(2)
    print(f"[Celery Test] Task completed successfully!")
    return f"Task completed: {message}"

@shared_task
def send_email_task(to_email, subject, body):
    print(f"[Celery Email] Sending email to {to_email}")
    print(f"[Celery Email] Subject: {subject}")
    sleep(1)
    return f"Email sent to {to_email}"

@shared_task
def process_whatsapp_message(phone, message):
    print(f"[Celery WhatsApp] Sending message to {phone}")
    print(f"[Celery WhatsApp] Message: {message}")
    sleep(1)
    return f"WhatsApp message sent to {phone}"
