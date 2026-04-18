# bot/handlers/tmc_fsm_handler.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# FSM для ТМЦ
class TMCStates(StatesGroup):
    waiting_for_number = State()
    waiting_for_name = State()
    waiting_for_serial = State()
    waiting_for_percent = State()
    waiting_for_amount = State()

router = Router()

@router.message(F.text.lower() == "тмц 50/50")
async def start_tmc_handler(message: Message, state: FSMContext):
    await message.answer("Введите номер выдачи 1С:")
    await state.set_state(TMCStates.waiting_for_number)

@router.message(TMCStates.waiting_for_number)
async def process_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Введите наименование ТМЦ:")
    await state.set_state(TMCStates.waiting_for_name)

@router.message(TMCStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите серийный номер:")
    await state.set_state(TMCStates.waiting_for_serial)

@router.message(TMCStates.waiting_for_serial)
async def process_serial(message: Message, state: FSMContext):
    await state.update_data(serial=message.text)
    await message.answer("Введите соотношение (%):")
    await state.set_state(TMCStates.waiting_for_percent)

@router.message(TMCStates.waiting_for_percent)
async def process_percent(message: Message, state: FSMContext):
    await state.update_data(percent=message.text)
    await message.answer("Введите сумму:")
    await state.set_state(TMCStates.waiting_for_amount)

@router.message(TMCStates.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    data['amount'] = message.text
    await message.answer(f"✅ ТМЦ сохранено: {data}")
    await state.clear()

def register_tmc_handlers(dp):
    dp.include_router(router)
