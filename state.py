from aiogram.dispatcher.filters.state import StatesGroup, State

class Register(StatesGroup):
    uz_name = State()
    uz_phone_number = State()
    ru_name = State()
    ru_phone_number = State()
    en_name = State()
    en_phone_number = State()

class Weather(StatesGroup):
    uzbek = State()
    russian = State()
    english = State()

class Course(StatesGroup):
    uzbek = State()
    russian = State()
    english = State()

class ChangeLanguage(StatesGroup):
    uzbek = State()
    russian = State()
    english = State()