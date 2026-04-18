# bot/config.py

import os
import json

# -----------------------------
# Telegram
# -----------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OWNER_CHAT_ID = int(os.environ.get("OWNER_CHAT_ID", 0))

# -----------------------------
# Google Sheets
# -----------------------------
SHEET_CONNECTIONS = {
    "connection_bills": os.environ.get("GSHEET_CONNECTION_BILLS"),
    "tmc": os.environ.get("GSHEET_TMC"),
    "mfu": os.environ.get("GSHEET_MFU")
}

# Листы
SHEET_TMC_TAB = os.environ.get("SHEET_TMC_TAB", "ТМЦ 50/50")
SHEET_MFU_TAB = os.environ.get("SHEET_MFU_TAB", "МФУ")

# -----------------------------
# SMTP Mail
# -----------------------------
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.mail.ru")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 465))

# -----------------------------
# Google Service Account JSON
# -----------------------------
# Храните JSON в виде строки в переменной среды
GSERVICE_JSON_STR = os.environ.get("GSERVICE_JSON")
GSERVICE_JSON = json.loads(GSERVICE_JSON_STR) if GSERVICE_JSON_STR else None