# bot/handlers/reports_handler.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

# Простейший словарь для хранения отчетов в памяти (можно заменить на базу)
reports_storage = {}

@router.message(Command(commands=["report_add"]))
async def add_report(message: types.Message, state: FSMContext):
    """
    Добавляет отчет в память.
    Формат: /report_add Название_отчета | Текст отчета
    """
    try:
        text = message.text.split(" ", 1)[1]
        name, content = map(str.strip, text.split("|", 1))
        reports_storage[name] = content
        await message.answer(f"✅ Отчет '{name}' сохранен.")
    except Exception:
        await message.answer("❌ Используйте формат: /report_add Название_отчета | Текст отчета")

@router.message(Command(commands=["report_list"]))
async def list_reports(message: types.Message):
    """
    Показывает список всех отчетов
    """
    if not reports_storage:
        await message.answer("📂 Нет сохраненных отчетов")
        return
    response = "📋 Список отчетов:\n"
    for name, content in reports_storage.items():
        response += f"• {name}: {content}\n"
    await message.answer(response)

def register_reports_handlers(dp):
    """
    Функция для совместимости с main.py
    """
    dp.include_router(router)
