# bot/handlers/payment_handler.py

from aiogram import types, Dispatcher
from bot.services import payment_checker

async def check_payments_start(message: types.Message):
    await message.answer("Вставьте текст реестра оплат:")
    await message.bot.set_state(message.from_user.id, "waiting_registry_text")

async def perform_check_payments(message: types.Message, state):
    text = message.text
    results = payment_checker.check_payments(text)
    output = []
    for r in results:
        output.append(f"{r['№']} от {r['Дата']} | {r['Контрагент']} | {r['Сумма']} | {r['Статус']}")
    await message.answer("\n".join(output))
    await state.finish()

def register_payment_handlers(dp: Dispatcher):
    dp.register_message_handler(check_payments_start, lambda m: m.text == "Статус оплаты")
    dp.register_message_handler(perform_check_payments, state="waiting_registry_text")