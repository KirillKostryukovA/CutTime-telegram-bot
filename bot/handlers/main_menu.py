from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command, CommandStart

import bot.keyboards.inline_keyboards as inl_kb

router = Router()


# Главное меню через команду Start
@router.message(CommandStart)
async def main_menu_user(message: Message):
    await message.answer(f"""
Привет, {message.from_user.first_name}! 👋 Добро пожаловать в CutTime — бот записи к барберу.

Выбирай свободный слот — и ты записан. Бот напомнит о визите и даст отменить запись, если планы поменялись.

Что хочешь сделать?

✂️ Записаться
📋 Мои записи
💬 Техподдержка
""", reply_markup=inl_kb.main_manu_kb)