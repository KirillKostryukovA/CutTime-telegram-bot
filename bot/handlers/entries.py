from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup

router = Router()


@router.callback_query(F.data == "sign_up")
async def sign_up():
    pass