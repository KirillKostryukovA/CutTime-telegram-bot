from datetime import datetime, time

from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    text,
    ForeignKey,
    Text,
    SmallInteger,
    Enum as SqlEnum,
    column,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint, TSTZRANGE
from sqlalchemy.orm import Mapped, mapped_column, relationship
from domain.enums import ServiceType, DayOfWeek, BookingStatus
from infrastructure.database import Base


# Информацию о пользователе
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    full_name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(12), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    )

    # Связь one2one с барбером
    master_info: Mapped["Master"] = relationship(back_populates="user_info")
    # Связь one2many с бронью
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")


# Профиль барбера (описание, таймзона, активность)
class Master(Base):
    __tablename__ = "masters"

    master_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), unique=True
    )
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    timezone: Mapped[str] = mapped_column(
        String(64), default="Europe/Moscow", nullable=False
    )
    # С каким шагом нарезать свободные слоты
    slot_step_minutes: Mapped[int] = mapped_column(
        SmallInteger, default=30, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    )

    # Связь one2one с пользователем
    user_info: Mapped["User"] = relationship(back_populates="master_info")
    # Связь one2many с услугами
    services: Mapped[list["Service"]] = relationship(back_populates="master")
    # Связь one2many с расписанием
    working_hours: Mapped[list["WorkingHour"]] = relationship(back_populates="master")
    # Связь one2many с бронью
    bookings: Mapped[list["Booking"]] = relationship(back_populates="master")


# Услуги мастера (Стрижка волос, бороды, бровей)
class Service(Base):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(primary_key=True)
    master_id: Mapped[int] = mapped_column(
        ForeignKey("masters.master_id", ondelete="CASCADE"), nullable=False
    )
    address: Mapped[str] = mapped_column(String(64), nullable=False)
    service_type: Mapped[ServiceType] = mapped_column(
        SqlEnum(ServiceType, name="service_type"), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    )

    # one2one связь с бабером
    master: Mapped["Master"] = relationship(back_populates="services")
    # one2many связь с бронью
    bookings: Mapped[list["Booking"]] = relationship(back_populates="service")


# Расписание мастера
class WorkingHour(Base):
    __tablename__ = "working_hours"

    working_id: Mapped[int] = mapped_column(primary_key=True)
    master_id: Mapped[int] = mapped_column(
        ForeignKey("masters.master_id", ondelete="CASCADE"), nullable=False
    )
    day_of_week: Mapped[DayOfWeek] = mapped_column(
        SqlEnum(DayOfWeek, name="day_of_week"), nullable=False
    )
    time_start: Mapped[time] = mapped_column(nullable=False)
    time_end: Mapped[time] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    )

    # Связь one2one схемы с схемой мастера
    master: Mapped["Master"] = relationship(back_populates="working_hours")
    bookings: Mapped["Booking"] = relationship(back_populates="working")
 

# Бронирование записи от лица пользователя
class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[int] = mapped_column(primary_key=True)
    master_id: Mapped[int] = mapped_column(
        ForeignKey("masters.master_id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.service_id", ondelete="CASCADE"), nullable=False
    )
    working_id: Mapped[int] = mapped_column(
        ForeignKey("working_hours.working_id", ondelete="CASCADE"), nullable=False
    )
    # Фиксирование цены за все услуги на момент создания записи
    price_snapshot: Mapped[int] = mapped_column(Integer, nullable=False)
    # Статус брони
    status: Mapped["BookingStatus"] = mapped_column(
        SqlEnum(BookingStatus, name="booking_status")
    )
    slot_range: Mapped[object] = mapped_column(TSTZRANGE(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    )

    # Связь one2one с пользователем
    user: Mapped["User"] = relationship(back_populates="bookings")
    # Связь one2one с барбером
    master: Mapped["Master"] = relationship(back_populates="bookings")
    # Связь one2one с услугами
    service: Mapped["Service"] = relationship(back_populates="bookings")
    # Связь one2one с расписанием
    working: Mapped["WorkingHour"] = relationship(back_populates="bookings")

    # Запрещаем пересечение отрезков времени && у одного и того же мастера = , чтобы не было одновременной брони у 2-х пользователей
    __table_args__ = (
        ExcludeConstraint(
            (column("master_id"), "="),
            (column("slot_range"), "&&"),
            name="excl_bookings_master_slot_overlap",
            using="gist",
            where=text("status IN ('confirmed', 'in_process')"),
        ),
    )
