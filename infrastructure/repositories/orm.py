from sqlalchemy import select

from infrastructure.database import Base, async_session
from infrastructure.models import User


class AsyncOrm():
    @staticmethod
    async def add_user(tg_id: int):
        async with async_session() as session:
            """ После /start добавляем пользователя в базу данных """
            sqrt = await session.execute(select(User).where(User.tg_id == tg_id))
            user = sqrt.scalar_one_or_none()

            if user is None:
                new_user = User(tg_id=tg_id)
                
                session.add(new_user)
                await session.commit()