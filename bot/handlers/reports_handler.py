# bot/handlers/reports_handler.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import datetime

router = Router()

class ReportStates(StatesGroup):
    waiting_for_text = State()

async def create_report(message: Message, state: FSMContext):
    await message.answer("Введите текст отчета:")
    await state.set_state(ReportStates.waiting_for_text)

async def save_report(message: Message, state: FSMContext):
    await state.update_data(text=message.text, date=datetime.datetime.now())
    data = await state.get_data()
    await message.answer(f"Отчет сохранен на месяц: {data['text']}")
    await state.clear()

def register_reports_handlers(dp, storage):
    dp.message.register(create_report, F.text == "Создать отчет")
    dp.message.register(save_report, ReportStates.waiting_for_text)
