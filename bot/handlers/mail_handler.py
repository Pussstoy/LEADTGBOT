# bot/handlers/mail_handler.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()

async def check_mail(message: Message):
    # Заглушка: здесь будет логика поиска по почте
    await message.answer("Проверка почты запущена. Функция будет добавлена.")

def register_mail_handlers(dp):
    dp.message.register(check_mail, F.text == "Почта")
