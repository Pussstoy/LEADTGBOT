# bot/services/tmc_service.py

tmc_records = []

def add_tmc(record: dict):
    tmc_records.append(record)

def get_tmc_by_number_and_date(number: str, date: str):
    for r in tmc_records:
        if r.get("Номер выдачи 1С") == number and r.get("Дата") == date:
            return r
    return None

def search_tmc(query: str):
    results = []
    for r in tmc_records:
        if query in r.values():
            results.append(r)
    return results