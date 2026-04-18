# bot/handlers/payment_handler.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

# FSM для проверки оплат
class PaymentStates(StatesGroup):
    waiting_for_registry = State()

@router.message(F.text.lower() == "статус оплаты")
async def start_payment_check(message: Message, state: FSMContext):
    await message.answer("Вставьте текст реестра оплат:")
    await state.set_state(PaymentStates.waiting_for_registry)

@router.message(PaymentStates.waiting_for_registry)
async def process_registry(message: Message, state: FSMContext):
    registry_text = message.text
    
    # Здесь должна быть логика поиска совпадений с базой счетов и заявок
    # Для примера выводим просто текст реестра
    await message.answer(f"✅ Реестр принят, обработка...\n{text[:500]}... (сокращено)")

    # TODO: сверка по номерам и датам, кроме счетов за связь
    await state.clear()

def register_payment_handlers(dp):
    dp.include_router(router)
