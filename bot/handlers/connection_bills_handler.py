# bot/handlers/connection_bills_handler.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

# Пример состояний для счетов
class ConnectionBillStates(StatesGroup):
    waiting_for_number = State()
    waiting_for_date = State()
    waiting_for_amount = State()

async def start_connection_bill(message: Message, state: FSMContext):
    await message.answer("Введите номер счета:")
    await state.set_state(ConnectionBillStates.waiting_for_number)

async def get_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Введите дату счета (ДД.ММ.ГГГГ):")
    await state.set_state(ConnectionBillStates.waiting_for_date)

async def get_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введите сумму:")
    await state.set_state(ConnectionBillStates.waiting_for_amount)

async def get_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    await message.answer(
        f"Счет сохранен:\nНомер: {data['number']}\nДата: {data['date']}\nСумма: {data['amount']}"
    )
    await state.clear()

def register_connection_bills_handlers(dp):
    dp.message.register(start_connection_bill, F.text == "Создать счет")
    dp.message.register(get_number, ConnectionBillStates.waiting_for_number)
    dp.message.register(get_date, ConnectionBillStates.waiting_for_date)
    dp.message.register(get_amount, ConnectionBillStates.waiting_for_amount)
