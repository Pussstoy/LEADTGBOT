# bot/services/google_sheets.py

import gspread
from bot import config
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# -----------------------------
# Авторизация в Google Sheets
# -----------------------------
def get_gspread_client():
    if not config.GSERVICE_JSON:
        raise ValueError("Google Service Account JSON не задан")
    client = gspread.service_account_from_dict(config.GSERVICE_JSON)
    return client

# -----------------------------
# Получение всех счетов за связь
# -----------------------------
def get_connection_bills_all():
    client = get_gspread_client()
    sh = client.open_by_key(config.SHEET_CONNECTIONS["connection_bills"])
    # Получаем список листов
    worksheets = sh.worksheets()
    # Последний лист по дате создания
    active_sheet = worksheets[-1]
    rows = active_sheet.get_all_records()
    return rows, active_sheet.title

# -----------------------------
# Получение неоплаченных счетов
# -----------------------------
def get_unpaid_connection_bills():
    rows, sheet_name = get_connection_bills_all()
    unpaid = [row for row in rows if not row.get('Сумма')]  # Пустой столбец суммы
    return unpaid

# -----------------------------
# Создание нового листа (копия последнего)
# -----------------------------
def create_new_connection_bills_sheet():
    client = get_gspread_client()
    sh = client.open_by_key(config.SHEET_CONNECTIONS["connection_bills"])
    last_sheet = sh.worksheets()[-1]
    # Имя нового листа: следующий месяц yyyy.mm
    last_title = last_sheet.title
    try:
        last_date = datetime.strptime(last_title, "%Y.%m")
    except ValueError:
        last_date = datetime.now()
    # Следующий месяц
    month = last_date.month + 1
    year = last_date.year
    if month > 12:
        month = 1
        year += 1
    new_sheet_name = f"{year}.{month:02d}"
    # Создание копии
    new_sheet = sh.duplicate_sheet(last_sheet.id, new_sheet_name=new_sheet_name)
    # Очищаем столбец B (Сумма)
    cell_range = f"B2:B{new_sheet.row_count}"
    new_sheet.batch_clear([cell_range])
    return new_sheet_name

def enter_amount_connection_bill(number, amount):
    client = get_gspread_client()
    sh = client.open_by_key(config.SHEET_CONNECTIONS["connection_bills"])
    sheet = sh.worksheets()[-1]  # последний активный лист
    records = sheet.get_all_records()
    for idx, row in enumerate(records, start=2):  # строки начинаются с 2, так как row 1 — заголовок
        if str(row.get("№")) == str(number):
            cell = f"B{idx}"  # столбец B — сумма
            sheet.update(cell, amount)
            return True
    return False

# bot/services/google_sheets.py

# -----------------------------
# Получение всех записей ТМЦ 50/50
# -----------------------------
def get_tmc_all():
    client = get_gspread_client()
    sh = client.open_by_key(config.SHEET_TMC["tmc"])
    sheet = sh.worksheet("ТМЦ 50/50")
    return sheet.get_all_records()

# -----------------------------
# Добавление новой записи ТМЦ
# -----------------------------
def create_tmc_record(record: dict):
    """
    record - словарь с ключами:
    'Номер выдачи 1С', 'Наименование ТМЦ', 'ФИО', 'Серийный номер',
    'Соотношение (%)', 'Сумма', 'Номер + дата счета', 'Номер договора', 'Состояние выдачи'
    """
    client = get_gspread_client()
    sh = client.open_by_key(config.SHEET_TMC["tmc"])
    sheet = sh.worksheet("ТМЦ 50/50")
    row = [
        record.get("Номер выдачи 1С", ""),
        record.get("Наименование ТМЦ", ""),
        record.get("ФИО", ""),
        record.get("Серийный номер", ""),
        record.get("Соотношение (%)", ""),
        record.get("Сумма", ""),
        record.get("Номер + дата счета", ""),
        record.get("Номер договора", ""),
        record.get("Состояние выдачи", "")
    ]
    sheet.append_row(row)

# -----------------------------
# Поиск записей ТМЦ
# -----------------------------
def search_tmc_records(query: str):
    """
    Ищет по номеру, дате, серийному номеру
    """
    records = get_tmc_all()
    results = []
    for row in records:
        if (query in str(row.get("Номер выдачи 1С",""))) or \
           (query in str(row.get("Номер + дата счета",""))) or \
           (query in str(row.get("Серийный номер",""))):
            results.append(row)
    return results

# bot/services/google_sheets.py

# -----------------------------
# Получение всех записей МФУ
# -----------------------------
def get_mfu_all():
    client = get_gspread_client()
    sh = client.open_by_key(config.SHEET_MFU["mfu"])
    sheet = sh.worksheet("МФУ")
    return sheet.get_all_records()

# -----------------------------
# Добавление новой записи МФУ
# -----------------------------
def create_mfu_record(record: dict):
    """
    record - словарь с ключами:
    'Производитель', 'Модель', 'Серийный номер', 'Откуда приехал', 
    'Кому выдан', 'Состояние', 'Тип принтера', 'Формат печати', 'Монохром / Цвет'
    """
    client = get_gspread_client()
    sh = client.open_by_key(config.SHEET_MFU["mfu"])
    sheet = sh.worksheet("МФУ")
    row = [
        record.get("Производитель", ""),
        record.get("Модель", ""),
        record.get("Серийный номер", ""),
        record.get("Откуда приехал", ""),
        record.get("Кому выдан", ""),
        record.get("Состояние", ""),
        record.get("Тип принтера", ""),
        record.get("Формат печати", ""),
        record.get("Монохром / Цвет", "")
    ]
    sheet.append_row(row)

# -----------------------------
# Поиск записей МФУ по серийному номеру
# -----------------------------
def search_mfu_records(sn: str):
    records = get_mfu_all()
    results = []
    for row in records:
        if sn in str(row.get("Серийный номер","")):
            results.append(row)
    return results