from aiogram import types
from aiogram.dispatcher import FSMContext

def get_start_menu() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="✳️Add repo"),
            types.KeyboardButton(text="❌Remove repo")
        ],
        [
            types.KeyboardButton(text="📋List repos")
        ]
    ]
    start_keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return start_keyboard


async def start(message: types.Message, state: FSMContext):
    keyboard = get_start_menu()

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await message.answer("Hi! I am MaintainerBot and my main ability is to notify " + \
        "you about new project releases!")
    await message.answer("How can I help you?", reply_markup=keyboard)

async def home(message: types.Message, state: FSMContext):
    keyboard = get_start_menu()

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await message.answer("How can I help you?", reply_markup=keyboard)