# bot/handlers/mail_handler.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import imaplib
import email
import os

# FSM для поиска почты
class MailStates(StatesGroup):
    waiting_for_account = State()
    waiting_for_days = State()

router = Router()

@router.message(F.text.lower() == "почта")
async def start_mail_handler(message: Message, state: FSMContext):
    await message.answer("Введите Л/С или № заявки/счета для поиска:")
    await state.set_state(MailStates.waiting_for_account)

@router.message(MailStates.waiting_for_account)
async def process_account(message: Message, state: FSMContext):
    await state.update_data(account=message.text)
    await message.answer("Введите период поиска в днях (1/3/5/10/20):")
    await state.set_state(MailStates.waiting_for_days)

@router.message(MailStates.waiting_for_days)
async def process_days(message: Message, state: FSMContext):
    await state.update_data(days=int(message.text))
    data = await state.get_data()
    
    # подключение к Mail.ru бизнес через IMAP
    MAIL_USER = os.getenv("SMTP_USER")
    MAIL_PASS = os.getenv("SMTP_PASSWORD")
    try:
        mail = imaplib.IMAP4_SSL("imap.mail.ru")
        mail.login(MAIL_USER, MAIL_PASS)
        mail.select("INBOX")

        result, data_list = mail.search(None, 'ALL')
        messages = []
        for num in data_list[0].split():
            result, msg_data = mail.fetch(num, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            if data['account'] in msg.get("Subject", ""):
                messages.append(msg.get("Subject"))

        await message.answer(f"Найдено писем: {len(messages)}\n{messages}")
        mail.logout()
    except Exception as e:
        await message.answer(f"Ошибка подключения к почте: {e}")

    await state.clear()

def register_mail_handlers(dp):
    dp.include_router(router)
