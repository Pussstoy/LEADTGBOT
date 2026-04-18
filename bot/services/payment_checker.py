# bot/services/payment_checker.py

import re
from bot.services import connection_bills_service

def parse_payment_registry(text: str):
    """
    Разбор реестра оплат, возвращает список счетов с номером и датой
    Пример строки:
    "20523 от 09.04.2026 - ДНС РИТЕЙЛ ООО - 5 599,00 - Сузун Коммутаторы + Сетевая карта"
    """
    pattern = r"(\d+)\s+от\s+(\d{2}\.\d{2}\.\d{4})"
    matches = re.findall(pattern, text)
    return matches  # [('20523', '09.04.2026'), ...]

def check_payments(text: str):
    """
    Сверка всех счетов в базе с реестром
    """
    registry = parse_payment_registry(text)
    results = []

    all_bills = connection_bills_service.get_all_bills(exclude_communication=True)

    for bill in all_bills:
        bill_number = str(bill["№"])
        bill_date = bill["Дата"]
        if (bill_number, bill_date) in registry:
            status = "Оплачен"
        else:
            status = "Не оплачен"
        results.append({
            "№": bill_number,
            "Дата": bill_date,
            "Контрагент": bill["Контрагент"],
            "Сумма": bill["Сумма"],
            "Статус": status
        })
    return results