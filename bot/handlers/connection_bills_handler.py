# bot/handlers/connection_bills_handler.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.services import connection_bills_service

# -----------------------------
# Кнопки меню
# -----------------------------
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton("Счета за связь"))
kb_main.add(KeyboardButton("Счета к заявкам"))

# -----------------------------
# Команды и кнопки
# -----------------------------
async def start_handler(message: types.Message):
    await message.answer("Выберите раздел:", reply_markup=kb_main)

async def view_connection_bills(message: types.Message):
    bills = connection_bills_service.communication_bills
    if not bills:
        await message.answer("Счетов за связь пока нет.")
        return
    output = []
    for b in bills:
        output.append(f"{b['№']} от {b['Дата']} | {b.get('Контрагент','')} | {b.get('Сумма','')}")
    await message.answer("\n".join(output))

# -----------------------------
# Регистрация обработчиков
# -----------------------------
def register_connection_bills_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(view_connection_bills, lambda m: m.text == "Счета за связь")