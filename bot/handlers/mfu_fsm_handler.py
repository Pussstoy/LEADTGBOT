# bot/handlers/mfu_fsm_handler.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.services import mfu_service

class MFUStates(StatesGroup):
    waiting_manufacturer = State()
    waiting_model = State()
    waiting_serial = State()

async def start_mfu(message: types.Message):
    await message.answer("Введите производителя МФУ:")
    await MFUStates.waiting_manufacturer.set()

async def mfu_manufacturer(message: types.Message, state: FSMContext):
    await state.update_data(manufacturer=message.text)
    await message.answer("Введите модель МФУ:")
    await MFUStates.waiting_model.set()

async def mfu_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите серийный номер МФУ:")
    await MFUStates.waiting_serial.set()

async def mfu_serial(message: types.Message, state: FSMContext):
    data = await state.get_data()
    record = {
        "Производитель": data["manufacturer"],
        "Модель": data["model"],
        "Серийный номер": message.text
    }
    mfu_service.add_mfu(record)
    await message.answer("✅ МФУ добавлен.")
    await state.finish()

def register_mfu_handlers(dp: Dispatcher):
    dp.register_message_handler(start_mfu, lambda m: m.text == "МФУ")
    dp.register_message_handler(mfu_manufacturer, state=MFUStates.waiting_manufacturer)
    dp.register_message_handler(mfu_model, state=MFUStates.waiting_model)
    dp.register_message_handler(mfu_serial, state=MFUStates.waiting_serial)