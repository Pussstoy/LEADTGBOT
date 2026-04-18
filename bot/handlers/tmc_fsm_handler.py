# bot/handlers/tmc_fsm_handler.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.services import tmc_service

class TMCStates(StatesGroup):
    waiting_number = State()
    waiting_date = State()
    waiting_description = State()

async def start_tmc(message: types.Message):
    await message.answer("Введите номер ТМЦ:")
    await TMCStates.waiting_number.set()

async def tmc_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Введите дату выдачи ТМЦ (ДД.ММ.ГГГГ):")
    await TMCStates.waiting_date.set()

async def tmc_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введите описание ТМЦ:")
    await TMCStates.waiting_description.set()

async def tmc_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tmc_record = {
        "Номер выдачи 1С": data["number"],
        "Дата": data["date"],
        "Описание": message.text
    }
    tmc_service.add_tmc(tmc_record)
    await message.answer("✅ ТМЦ добавлен.")
    await state.finish()

def register_tmc_handlers(dp: Dispatcher):
    dp.register_message_handler(start_tmc, lambda m: m.text == "ТМЦ 50/50")
    dp.register_message_handler(tmc_number, state=TMCStates.waiting_number)
    dp.register_message_handler(tmc_date, state=TMCStates.waiting_date)
    dp.register_message_handler(tmc_description, state=TMCStates.waiting_description)