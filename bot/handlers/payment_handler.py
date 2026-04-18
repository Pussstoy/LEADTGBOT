# bot/handlers/payment_handler.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()

async def check_payment(message: Message):
    # Заглушка: логика сверки с реестром оплат
    await message.answer("Проверка оплаты запущена. Функция будет добавлена.")

def register_payment_handlers(dp):
    dp.message.register(check_payment, F.text == "Статус оплаты")
