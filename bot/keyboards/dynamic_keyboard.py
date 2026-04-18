# bot/keyboards/dynamic_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def choose_from_list_keyboard(items, key="number"):
    """
    Создает Inline клавиатуру для выбора одного элемента из списка
    items: list[dict] - список словарей с данными
    key: str - ключ для отображения и callback_data
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in items:
        display_text = item.get(key, "Без имени")
        callback_value = f"select_{item.get(key)}"
        keyboard.add(InlineKeyboardButton(display_text, callback_data=callback_value))
    return keyboard