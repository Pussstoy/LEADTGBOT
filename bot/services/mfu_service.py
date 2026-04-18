# bot/services/mfu_service.py

mfu_records = []

def add_mfu(record: dict):
    mfu_records.append(record)

def get_mfu_by_serial(serial: str):
    for r in mfu_records:
        if r.get("Серийный номер") == serial:
            return r
    return None

def filter_mfu(state=None, format_print=None, color=None):
    results = []
    for r in mfu_records:
        if state and r.get("Состояние") != state:
            continue
        if format_print and r.get("Формат печати") != format_print:
            continue
        if color and r.get("Монохром / Цвет") != color:
            continue
        results.append(r)
    return results