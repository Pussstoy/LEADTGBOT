# bot/handlers/tmc_fsm_handler.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class TMCStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_serial = State()
    waiting_for_amount = State()

async def start_tmc(message: Message, state: FSMContext):
    await message.answer("Введите наименование ТМЦ:")
    await state.set_state(TMCStates.waiting_for_name)

async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите серийный номер:")
    await state.set_state(TMCStates.waiting_for_serial)

async def get_serial(message: Message, state: FSMContext):
    await state.update_data(serial=message.text)
    await message.answer("Введите сумму:")
    await state.set_state(TMCStates.waiting_for_amount)

async def get_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    await message.answer(
        f"ТМЦ сохранено:\nНаименование: {data['name']}\nСерийный номер: {data['serial']}\nСумма: {data['amount']}"
    )
    await state.clear()

def register_tmc_handlers(dp):
    dp.message.register(start_tmc, F.text == "Создать ТМЦ")
    dp.message.register(get_name, TMCStates.waiting_for_name)
    dp.message.register(get_serial, TMCStates.waiting_for_serial)
    dp.message.register(get_amount, TMCStates.waiting_for_amount)
