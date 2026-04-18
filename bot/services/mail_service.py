# bot/services/mail_service.py

import imaplib
import email
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

MAIL_USER = os.getenv("SMTP_USER")
MAIL_PASS = os.getenv("SMTP_PASSWORD")
MAIL_HOST = "imap.mail.ru"  # Mail.ru IMAP сервер

# -----------------------------
# Подключение к почте
# -----------------------------
def connect_mail():
    try:
        mail = imaplib.IMAP4_SSL(MAIL_HOST)
        mail.login(MAIL_USER, MAIL_PASS)
        logger.info("Подключение к почте успешно")
        return mail
    except Exception as e:
        logger.error(f"Ошибка подключения к почте: {e}")
        return None

# -----------------------------
# Поиск писем за последние N дней по запросу
# -----------------------------
def search_emails(query: str, days: int = 5):
    mail = connect_mail()
    if not mail:
        return []

    mail.select("INBOX")
    since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    search_criterion = f'(SINCE "{since_date}" BODY "{query}")'

    try:
        result, data = mail.search(None, search_criterion)
        if result != 'OK':
            logger.warning("Не удалось выполнить поиск")
            return []

        email_ids = data[0].split()
        emails = []

        for eid in email_ids:
            res, msg_data = mail.fetch(eid, "(RFC822)")
            if res != 'OK':
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            emails.append(parse_email_content(msg))

        mail.logout()
        return emails

    except Exception as e:
        logger.error(f"Ошибка при поиске писем: {e}")
        return []

# -----------------------------
# Разбор письма
# -----------------------------
def parse_email_content(msg):
    subject = msg.get("subject", "")
    from_email = msg.get("from", "")
    date_email = msg.get("date", "")
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors='ignore')
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')
    return {
        "subject": subject,
        "from": from_email,
        "date": date_email,
        "body": body
    }