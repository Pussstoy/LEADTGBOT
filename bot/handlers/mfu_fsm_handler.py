# bot/handlers/mfu_fsm_handler.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# FSM для МФУ
class MFUStates(StatesGroup):
    waiting_for_manufacturer = State()
    waiting_for_model = State()
    waiting_for_serial = State()
    waiting_for_from = State()
    waiting_for_to = State()
    waiting_for_status = State()
    waiting_for_type = State()
    waiting_for_format = State()
    waiting_for_color = State()

router = Router()

@router.message(F.text.lower() == "мфу")
async def start_mfu_handler(message: Message, state: FSMContext):
    await message.answer("Введите производителя:")
    await state.set_state(MFUStates.waiting_for_manufacturer)

@router.message(MFUStates.waiting_for_manufacturer)
async def process_manufacturer(message: Message, state: FSMContext):
    await state.update_data(manufacturer=message.text)
    await message.answer("Введите модель:")
    await state.set_state(MFUStates.waiting_for_model)

@router.message(MFUStates.waiting_for_model)
async def process_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите серийный номер:")
    await state.set_state(MFUStates.waiting_for_serial)

@router.message(MFUStates.waiting_for_serial)
async def process_serial(message: Message, state: FSMContext):
    await state.update_data(serial=message.text)
    await message.answer("Откуда пришло:")
    await state.set_state(MFUStates.waiting_for_from)

@router.message(MFUStates.waiting_for_from)
async def process_from(message: Message, state: FSMContext):
    await state.update_data(from_location=message.text)
    await message.answer("Кому выдано:")
    await state.set_state(MFUStates.waiting_for_to)

@router.message(MFUStates.waiting_for_to)
async def process_to(message: Message, state: FSMContext):
    await state.update_data(to_person=message.text)
    await message.answer("Состояние:")
    await state.set_state(MFUStates.waiting_for_status)

@router.message(MFUStates.waiting_for_status)
async def process_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    await message.answer("Тип принтера:")
    await state.set_state(MFUStates.waiting_for_type)

@router.message(MFUStates.waiting_for_type)
async def process_type(message: Message, state: FSMContext):
    await state.update_data(type_printer=message.text)
    await message.answer("Формат печати:")
    await state.set_state(MFUStates.waiting_for_format)

@router.message(MFUStates.waiting_for_format)
async def process_format(message: Message, state: FSMContext):
    await state.update_data(format_print=message.text)
    await message.answer("Монохром или цвет?")
    await state.set_state(MFUStates.waiting_for_color)

@router.message(MFUStates.waiting_for_color)
async def process_color(message: Message, state: FSMContext):
    await state.update_data(color_type=message.text)
    data = await state.get_data()
    await message.answer(f"✅ МФУ сохранено: {data}")
    await state.clear()

def register_mfu_handlers(dp):
    dp.include_router(router)
