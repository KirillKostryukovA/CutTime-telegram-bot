from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

router = Router()


@router.callback_query(F.data == "sign_up")
async def sign_up(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text("Выберите дату")