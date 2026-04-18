# bot/main.py

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# -----------------------------
# Загрузка переменных окружения
# -----------------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")

if not BOT_TOKEN or not OWNER_CHAT_ID:
    raise ValueError("Не заданы переменные BOT_TOKEN или OWNER_CHAT_ID в .env")

# -----------------------------
# Настройка логирования
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Инициализация бота и FSM
# -----------------------------
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.bot = bot  # <-- важно присвоить экземпляр бота

# -----------------------------
# Импорт и регистрация обработчиков
# -----------------------------
from bot.handlers.connection_bills_handler import register_connection_bills_handlers
from bot.handlers.tmc_fsm_handler import register_tmc_handlers
from bot.handlers.mfu_fsm_handler import register_mfu_handlers
from bot.handlers.mail_handler import register_mail_handlers
from bot.handlers.payment_handler import register_payment_handlers
from bot.handlers.reports_handler import register_reports_handlers

register_connection_bills_handlers(dp)
register_tmc_handlers(dp)
register_mfu_handlers(dp)
register_mail_handlers(dp)
register_payment_handlers(dp)
register_reports_handlers(dp)

# -----------------------------
# Запуск бота
# -----------------------------
async def main():
    logger.info("Запуск бота...")
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
# -----------------------------
# Загрузка переменных окружения
# -----------------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")

if not BOT_TOKEN or not OWNER_CHAT_ID:
    raise ValueError("Не заданы переменные BOT_TOKEN или OWNER_CHAT_ID в .env")

# -----------------------------
# Настройка логирования
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Инициализация бота и FSM
# -----------------------------
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.bot = bot  # <-- важно присвоить экземпляр бота сюда

# -----------------------------
# Импорт и регистрация обработчиков
# -----------------------------
from bot.handlers.connection_bills_handler import register_connection_bills_handlers
from bot.handlers.tmc_fsm_handler import register_tmc_handlers
from bot.handlers.mfu_fsm_handler import register_mfu_handlers
from bot.handlers.mail_handler import register_mail_handlers
from bot.handlers.payment_handler import register_payment_handlers
from bot.handlers.reports_handler import register_reports_handlers

register_connection_bills_handlers(dp)
register_tmc_handlers(dp)
register_mfu_handlers(dp)
register_mail_handlers(dp)
register_payment_handlers(dp)
register_reports_handlers(dp)

# -----------------------------
# Автоперезапуск при ошибках
# -----------------------------
async def main():
    logger.info("Запуск бота...")
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
