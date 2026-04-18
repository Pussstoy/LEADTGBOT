# bot/services/reports_service.py

import sqlite3
from datetime import datetime, timedelta

DB_FILE = "reports.db"

# -----------------------------
# Инициализация базы
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            text TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# -----------------------------
# Добавление нового отчета
# -----------------------------
def add_report(name: str, text: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute('INSERT INTO reports (name, text, created_at) VALUES (?, ?, ?)', (name, text, created_at))
    conn.commit()
    conn.close()

# -----------------------------
# Получение всех отчетов
# -----------------------------
def get_reports():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, text, created_at FROM reports ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# -----------------------------
# Удаление отчетов старше 30 дней
# -----------------------------
def cleanup_old_reports():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cutoff = (datetime.now() - timedelta(days=30)).isoformat()
    cursor.execute('DELETE FROM reports WHERE created_at < ?', (cutoff,))
    conn.commit()
    conn.close()