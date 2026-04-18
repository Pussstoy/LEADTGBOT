# bot/handlers/mail_handler.py

from aiogram import types, Dispatcher
from bot.services import mail_service

async def mail_search(message: types.Message):
    await message.answer("Введите ключевое слово для поиска писем:")
    
    # Сохраняем состояние ожидания ввода
    await message.bot.set_state(message.from_user.id, "waiting_mail_query")

async def perform_mail_search(message: types.Message, state):
    query = message.text
    days = 10  # По умолчанию период поиска 10 дней
    results = mail_service.search_emails(query, days)
    
    if not results:
        await message.answer("Письма не найдены.")
    else:
        output = []
        for r in results:
            if "error" in r:
                output.append(f"Ошибка: {r['error']}")
            else:
                output.append(f"{r['date']} | {r['from']} | {r['subject']}")
        await message.answer("\n".join(output))
    await state.finish()

def register_mail_handlers(dp: Dispatcher):
    dp.register_message_handler(mail_search, lambda m: m.text == "Почта")
    dp.register_message_handler(perform_mail_search, state="waiting_mail_query")