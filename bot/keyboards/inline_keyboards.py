from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


main_manu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="✂️ Записаться",
        callback_data="sign_up",
    )],
    [InlineKeyboardButton(
        text="📋 Мои записи",
        callback_data="my_entries",
    )],
    [InlineKeyboardButton(
        text="💬 Техподдержка",
        callback_data="tech_support",
    )],
])