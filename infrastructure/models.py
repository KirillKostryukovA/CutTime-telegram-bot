import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import Base


# Схема, хранящая информацию о пользователе
class UserInfo(Base):
    __tablename__ = "user_info"

    info_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())