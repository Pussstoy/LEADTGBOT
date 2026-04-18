# bot/handlers/mfu_fsm_handler.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class MFUStates(StatesGroup):
    waiting_for_model = State()
    waiting_for_serial = State()
    waiting_for_status = State()

async def start_mfu(message: Message, state: FSMContext):
    await message.answer("Введите модель МФУ:")
    await state.set_state(MFUStates.waiting_for_model)

async def get_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите серийный номер:")
    await state.set_state(MFUStates.waiting_for_serial)

async def get_serial(message: Message, state: FSMContext):
    await state.update_data(serial=message.text)
    await message.answer("Введите состояние МФУ:")
    await state.set_state(MFUStates.waiting_for_status)

async def get_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    data = await state.get_data()
    await message.answer(
        f"МФУ сохранено:\nМодель: {data['model']}\nСерийный номер: {data['serial']}\nСостояние: {data['status']}"
    )
    await state.clear()

def register_mfu_handlers(dp):
    dp.message.register(start_mfu, F.text == "Создать МФУ")
    dp.message.register(get_model, MFUStates.waiting_for_model)
    dp.message.register(get_serial, MFUStates.waiting_for_serial)
    dp.message.register(get_status, MFUStates.waiting_for_status)
