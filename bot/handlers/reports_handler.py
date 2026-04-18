# bot/handlers/reports_handler.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.services import reports_service

class ReportStates(StatesGroup):
    waiting_name = State()
    waiting_text = State()

async def start_add_report(message: types.Message):
    await message.answer("Введите название отчета:")
    await ReportStates.waiting_name.set()

async def report_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите текст отчета:")
    await ReportStates.waiting_text.set()

async def report_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    reports_service.add_report(data["name"], message.text)
    await message.answer("✅ Отчет сохранен.")
    await state.finish()

async def view_reports(message: types.Message):
    reports_service.cleanup_old_reports()
    reports = reports_service.get_reports()
    if not reports:
        await message.answer("Отчетов пока нет.")
        return
    output = []
    for r in reports:
        output.append(f"{r[1]} | {r[3]} \n{r[2]}\n")
    await message.answer("\n".join(output))

def register_reports_handlers(dp: Dispatcher, storage):
    dp.register_message_handler(start_add_report, lambda m: m.text == "Отчеты")
    dp.register_message_handler(report_name, state=ReportStates.waiting_name)
    dp.register_message_handler(report_text, state=ReportStates.waiting_text)
    dp.register_message_handler(view_reports, lambda m: m.text == "Просмотр отчетов")