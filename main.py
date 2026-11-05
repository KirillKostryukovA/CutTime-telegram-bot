import logging
import asyncio

from infrastructure.database import engine, Base
from infrastructure.models import UserInfo
from bot.handlers.main_menu import router as menu_router

from src.config import bot, dp


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Начало работы Бота")

    dp.include_router(menu_router)
    await dp.start_polling(bot)
    

# app = FastAPI(lifespan=main)


# Запуск всей программы
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())