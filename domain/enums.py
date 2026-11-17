from enum import Enum


# Тип для задания услуг
class ServiceType(str, Enum):
    haircut = "Стрижка волос"
    hair_styling = "Укладка волос"
    hair_correction = "Коррекция волос"
    head_care = "Уход за головой"
    beard_trimming = "Стрижка бороды"


# День недели для записи
class DayOfWeek(str, Enum):
    monday = "Понедельник"
    tuesday = "Вторник"
    wednesday = "Среда"
    thursday = "Четверг"
    friday = "Пятница"
    saturday = "Суббота"
    sunday = "Воскресенье"


# Статус брони
class BookingStatus(str, Enum):
    confirmed = "Подтверждённый"
    cancelled_by_user = "Отменённый пользователем"
    cancelled_by_master = "Отменённый барбером"
    in_process = "В процессе"