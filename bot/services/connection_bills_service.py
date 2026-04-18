# bot/services/connection_bills_service.py

from datetime import datetime

# Имитация базы счетов
bills = []
communication_bills = []

def add_bill(bill: dict, communication=False):
    """
    Добавляем счет в общий список или счета за связь
    """
    if communication:
        communication_bills.append(bill)
    else:
        bills.append(bill)

def get_all_bills(exclude_communication=False):
    """
    Получаем все счета
    """
    if exclude_communication:
        return bills
    return bills + communication_bills

def get_all_search_terms():
    """
    Возвращает список всех уникальных номеров, ЛС и коротких имен для глобального поиска
    """
    terms = []
    for b in bills + communication_bills:
        if "№" in b:
            terms.append(str(b["№"]))
        if "ЛС" in b:
            terms.append(str(b["ЛС"]))
        if "Короткое имя" in b:
            terms.append(str(b["Короткое имя"]))
    return terms