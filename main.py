import logging
import asyncio

from sqlalchemy import text
from infrastructure.database import engine, Base
from infrastructure.models import User, Master, Service, WorkingHour, Booking
from bot.handlers.main_menu import router as menu_router
from bot.handlers.entries import router as entries_router

from src.config import bot, dp


async def main():
    async with engine.begin() as conn:
        # Включаем расширение, которое учит gist работать с integer
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist;"))

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Начало работы Бота")

    dp.include_router(menu_router)
    dp.include_router(entries_router)
    await dp.start_polling(bot)


# app = FastAPI(lifespan=main)


# Запуск всей программы
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
