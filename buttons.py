from aiogram.types import *

language_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🇺🇿 O'zbekcha")
        ],
        [
            KeyboardButton("🇷🇺 Русский")
        ],
        [
            KeyboardButton("🇺🇸 English")
        ]
    ], resize_keyboard=True)

uzbek_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ob-havo"),
            KeyboardButton("Kurslar")
        ],
        [
            KeyboardButton("Tilni o'zgartirish")
        ]
    ],resize_keyboard=True
)

russian_menu_markup = ReplyKeyboardMarkup(

    keyboard=[
        [
            KeyboardButton("Погода"),
            KeyboardButton("Курсы")
        ],
        [
            KeyboardButton("Изменить язык")
        ]
    ],resize_keyboard=True
)

english_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Weather"),
            KeyboardButton("Courses")
        ],
        [
            KeyboardButton("Change the language")
        ]
    ],resize_keyboard=True
)

phone_number_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Phone number", request_contact=True)
        ]
    ],resize_keyboard=True
)

uzbek_course_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("USD"),
            KeyboardButton("EUR")
        ],
        [
            KeyboardButton("RUB")
        ],
        [
            KeyboardButton("Boshqa")
        ],
        [
            KeyboardButton("Ortga")
        ]
    ], resize_keyboard=True)

uzbek_weather_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Toshkent"),
            KeyboardButton("Andijan")
        ],
        [
            KeyboardButton("Samarqand"),
            KeyboardButton("Fargona")
        ],
        [
            KeyboardButton("Urganch"),
            KeyboardButton("Namangan")
        ],
        [
            KeyboardButton("Jizzax"),
            KeyboardButton("Termiz")
        ],
        [
            KeyboardButton("Qashqadaryo"),
            KeyboardButton("Sirdaryo")
        ],
        [
            KeyboardButton("Buxoro"),
            KeyboardButton("Navoi")
        ],
        [
            KeyboardButton("Ortga")
        ]
    ],resize_keyboard=True)


russian_course_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("USD"),
            KeyboardButton("EUR")
        ],
        [
            KeyboardButton("RUB")
        ],
        [
            KeyboardButton("Другое")
        ],
        [
            KeyboardButton("Назад")
        ]
    ], resize_keyboard=True)

russian_weather_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ташкент"),
            KeyboardButton("Андижан")
        ],
        [
            KeyboardButton("Самарканд"),
            KeyboardButton("Фергана")
        ],
        [
            KeyboardButton("Ургенч"),
            KeyboardButton("Наманган")
        ],
        [
            KeyboardButton("Джизак"),
            KeyboardButton("Термез")
        ],
        [
            KeyboardButton("Карши"),
            KeyboardButton("Гулистан")
        ],
        [
            KeyboardButton("Бухара"),
            KeyboardButton("Навои")
        ],
        [
            KeyboardButton("Назад")
        ]
    ],resize_keyboard=True)


english_course_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("USD"),
            KeyboardButton("EUR")
        ],
        [
            KeyboardButton("RUB")
        ],
        [
            KeyboardButton("Other")
        ],
        [
            KeyboardButton("Back")
        ]
    ], resize_keyboard=True)

english_weather_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Tashkent"),
            KeyboardButton("Andijan")
        ],
        [
            KeyboardButton("Samarkand"),
            KeyboardButton("Ferghana")
        ],
        [
            KeyboardButton("Urgench"),
            KeyboardButton("Namangan")
        ],
        [
            KeyboardButton("Jizzakh"),
            KeyboardButton("Termez")
        ],
        [
            KeyboardButton("Qarshi"),
            KeyboardButton("Gulistan")
        ],
        [
            KeyboardButton("Bukhara"),
            KeyboardButton("Navoi")
        ],
        [
            KeyboardButton("Back")
        ]
    ],resize_keyboard=True)

exit = ReplyKeyboardRemove()