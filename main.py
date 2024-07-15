from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.dispatcher import FSMContext
from googletrans import Translator
import requests
from buttons import *
from state import *
from database import *


TOKEN = "7293279051:AAGf-Tzv2g_uYXgtkM_GT2T-2iXhHHlvTNQ"
PROXY_URL = "http://proxy.server:3128"
bot = Bot(token=TOKEN, proxy=PROXY_URL)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
translator = Translator()
respone = requests.get('https://cbu.uz/uz/arkhiv-kursov-valyut/json/').json()


def weather(country):
    weather = requests.get(
        url=f"https://api.openweathermap.org/data/2.5/weather?q={country}&appid=fe3bf8a37354b57c77666e96b501efc9").json()
    return weather


async def on_startup(dp):
    create_tables()
    await bot.send_message(chat_id=1736508076, text="Bot has started")


async def on_shutdown(dp):
    await bot.send_message(chat_id=1736508076, text="Bot has stopped")

@dp.message_handler(commands=["start"])
async def start_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user = check_user(chat_id)
    if user:
        if user[4] == "UZ":
            await message.answer(f"Assalomu alaykum {user[2]}", reply_markup=uzbek_menu_markup)
        elif user[4] == "RU":
            await message.answer(f"Здравствуйте {user[2]}", reply_markup=russian_menu_markup)
        elif user[4] == "EN":
            await message.answer(f"Hello {user[2]}", reply_markup=english_menu_markup)
    else:
        await state.update_data(chat_id=chat_id)
        await message.answer("""
Salom! Ob-havo yoki kurs botiga xush kelibsiz.
Привет! Добро пожаловать в бот погоды или курса.
Hello! Welcome to weather or course bot.
""")
        await message.answer("""
Tilni tanlang.
Выберите язык.
Select a language.""", reply_markup=language_markup)

@dp.message_handler(text="🇺🇿 O'zbekcha")
async def language1_hanler(message: Message, state: FSMContext):
    await state.update_data(language="UZ")
    await message.answer("Siz o'zbek tilini tanladingiz.")
    await message.answer("Ismingizni kiriting.")
    await Register.uz_name.set()

@dp.message_handler(state=Register.uz_name)
async def uz_name_handler(message: Message, state: FSMContext):
    uz_name = message.text
    await state.update_data(name=uz_name)
    await message.answer("Telefon raqamingizni kiriting.", reply_markup=phone_number_markup)
    await Register.uz_phone_number.set()

@dp.message_handler(state=Register.uz_phone_number, content_types=types.ContentType.CONTACT)
async def uz_phone_number_handler(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    add_user(data=data)
    await message.answer("Siz registratsiya jarayonidan muvaffaqqiyatli o'tingiz.", reply_markup=uzbek_menu_markup)

@dp.message_handler(text="🇷🇺 Русский")
async def language2_hanler(message: Message, state: FSMContext):
    await state.update_data(language="RU")
    await message.answer("Вы выбрали русский.")
    await message.answer("Введите ваше имя.")
    await Register.ru_name.set()

@dp.message_handler(state=Register.ru_name)
async def ru_name_handler(message: Message, state: FSMContext):
    ru_name = message.text
    await state.update_data(name=ru_name)
    await message.answer("Введите свой номер телефона.", reply_markup=phone_number_markup)
    await Register.ru_phone_number.set()

@dp.message_handler(state=Register.ru_phone_number, content_types=types.ContentType.CONTACT)
async def ru_phone_number_handler(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    add_user(data=data)
    await message.answer("Вы успешно завершили процесс регистрации.", reply_markup=russian_menu_markup)
    await state.finish()

@dp.message_handler(text="🇺🇸 English")
async def language3_hanler(message: Message, state: FSMContext):
    await state.update_data(language="EN")
    await message.answer("You have selected English.")
    await message.answer("Enter your name.")
    await Register.en_name.set()

@dp.message_handler(state=Register.en_name)
async def en_name_handler(message: Message, state: FSMContext):
    en_name = message.text
    await state.update_data(name=en_name)
    await message.answer("Enter your phone number.", reply_markup=phone_number_markup)
    await Register.en_phone_number.set()

@dp.message_handler(state=Register.en_phone_number, content_types=types.ContentType.CONTACT)
async def en_phone_number_handler(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    add_user(data=data)
    await message.answer("You have successfully completed the registration process.", reply_markup=english_menu_markup)
    await state.finish()



@dp.message_handler(text="Ob-havo")
async def uz_weathers_handler(message: Message):
    await message.answer("Ob havo", reply_markup=uzbek_weather_markup)
    await Weather.uzbek.set()

@dp.message_handler(state=Weather.uzbek)
async def uz_weather_handler(message: Message, state: FSMContext):
    country_name = message.text
    if country_name == "Ortga":
        await message.answer("Tanlang",reply_markup=uzbek_menu_markup)
        await state.finish()
    else:
        weatherr = weather(country_name)
        description = weatherr['weather'][0]['description']
        temp = weatherr['main']['temp']
        wind_speed = weatherr['wind']['speed']
        result = translator.translate(description, dest="uz").text
        await message.answer(f"""
{country_name}:

Tavsif: {result}
Harorat: {int(temp - 273.15)} C°
Shamol tezligi: {wind_speed} m/s""")

@dp.message_handler(text="Kurslar")
async def uz_courses_handler(message: Message):
    await message.answer("Kurslar", reply_markup=uzbek_course_markup)
    await Course.uzbek.set()

@dp.message_handler(state=Course.uzbek)
async def uz_course_handler(message: Message, state: FSMContext):
    if message.text == "USD":
        text = "USD -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'USD':
                text += f"{course['CcyNm_UZ']} ----- {course['Rate']} so'm"
        await message.answer(text)
    elif message.text == "EUR":
        text = "EUR -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'EUR':
                text += f"{course['CcyNm_UZ']} ----- {course['Rate']} so'm"
        await message.answer(text)
    elif message.text == "RUB":
        text = "RUB -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'RUB':
                text += f"{course['CcyNm_UZ']} ----- {course['Rate']} so'm"
        await message.answer(text)
    elif message.text == "Boshqa":
        for course in respone:
            text = f"""
{course['Ccy']} -----> UZS
{course['CcyNm_UZ']} ----- {course['Rate']} so'm"""
            await message.answer(text)
    elif message.text == "Ortga":
        await message.answer("Tanlang", reply_markup=uzbek_menu_markup)
        await state.finish()

@dp.message_handler(text="Tilni o'zgartirish")
async def uz_change_languag_handler(message: Message):
    await message.answer("Tilni tanlang", reply_markup=language_markup)
    await ChangeLanguage.uzbek.set()

@dp.message_handler(state=ChangeLanguage.uzbek)
async def change_language_uz_handler(message: Message, state: FSMContext):
    if message.text == "🇺🇿 O'zbekcha":
        update_language(message.chat.id, "UZ")
        await message.answer("Siz o'zbekchani tanladingiz", reply_markup=uzbek_menu_markup)
    elif message.text == "🇷🇺 Русский":
        update_language(message.chat.id, "RU")
        await message.answer("Вы выбрали узбекский", reply_markup=russian_menu_markup)
    elif message.text == "🇺🇸 English":
        update_language(message.chat.id, "EN")
        await message.answer("You have chosen Uzbek", reply_markup=english_menu_markup)
    await state.finish()

@dp.message_handler(text="Погода")
async def ru_weathers_handler(message: Message):
    await message.answer("Погода", reply_markup=russian_weather_markup)
    await Weather.russian.set()

@dp.message_handler(state=Weather.russian)
async def ru_weather_handler(message: Message, state: FSMContext):
    country_name = message.text
    if country_name == "Назад":
        await message.answer("Выберите",reply_markup=russian_menu_markup)
        await state.finish()
    else:
        weatherr = weather(country_name)
        description = weatherr['weather'][0]['description']
        temp = weatherr['main']['temp']
        wind_speed = weatherr['wind']['speed']
        result = translator.translate(description, dest="ru").text
        await message.answer(f"""
{country_name}:

Описание: {result}
Температура: {int(temp - 273.15)} C°
Скорость ветра: {wind_speed} m/s""")

@dp.message_handler(text="Курсы")
async def ru_courses_handler(message: Message):
    await message.answer("Курсы", reply_markup=russian_course_markup)
    await Course.russian.set()

@dp.message_handler(state=Course.russian)
async def ru_course_handler(message: Message, state: FSMContext):
    if message.text == "USD":
        text = "USD -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'USD':
                text += f"{course['CcyNm_RU']} ----- {course['Rate']} сум"
        await message.answer(text)
    elif message.text == "EUR":
        text = "EUR -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'EUR':
                text += f"{course['CcyNm_RU']} ----- {course['Rate']} сум"
        await message.answer(text)
    elif message.text == "RUB":
        text = "RUB -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'RUB':
                text += f"{course['CcyNm_RU']} ----- {course['Rate']} сум"
        await message.answer(text)
    elif message.text == "Другое":
        for course in respone:
            text = f"""
{course['Ccy']} -----> UZS
{course['CcyNm_RU']} ----- {course['Rate']} сум"""
            await message.answer(text)
    elif message.text == "Назад":
        await message.answer("Выберите", reply_markup=russian_menu_markup)
        await state.finish()

@dp.message_handler(text="Изменить язык")
async def uz_change_languag_handler(message: Message):
    await message.answer("Изменить язык", reply_markup=language_markup)
    await ChangeLanguage.russian.set()

@dp.message_handler(state=ChangeLanguage.russian)
async def change_language_uz_handler(message: Message, state: FSMContext):
    if message.text == "🇺🇿 O'zbekcha":
        update_language(message.chat.id, "UZ")
        await message.answer("Siz o'zbekchani tanladingiz", reply_markup=uzbek_menu_markup)
    elif message.text == "🇷🇺 Русский":
        update_language(message.chat.id, "RU")
        await message.answer("Вы выбрали узбекский", reply_markup=russian_menu_markup)
    elif message.text == "🇺🇸 English":
        update_language(message.chat.id, "EN")
        await message.answer("You have chosen Uzbek", reply_markup=english_menu_markup)
    await state.finish()



@dp.message_handler(text="Weather")
async def ru_weathers_handler(message: Message):
    await message.answer("Weather", reply_markup=english_weather_markup)
    await Weather.english.set()

@dp.message_handler(state=Weather.english)
async def en_weather_handler(message: Message, state: FSMContext):
    country_name = message.text
    if country_name == "Back":
        await message.answer("Choose",reply_markup=english_menu_markup)
        await state.finish()
    else:
        weatherr = weather(country_name)
        description = weatherr['weather'][0]['description']
        temp = weatherr['main']['temp']
        wind_speed = weatherr['wind']['speed']
        await message.answer(f"""
{country_name}:

Description: {description}
Temperature: {int(temp - 273.15)} C°
Wind speed: {wind_speed} m/s""")

@dp.message_handler(text="Courses")
async def en_courses_handler(message: Message):
    await message.answer("Courses", reply_markup=english_course_markup)
    await Course.english.set()

@dp.message_handler(state=Course.english)
async def en_course_handler(message: Message, state: FSMContext):
    if message.text == "USD":
        text = "USD -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'USD':
                text += f"{course['CcyNm_EN']} ----- {course['Rate']} soum"
        await message.answer(text)
    elif message.text == "EUR":
        text = "EUR -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'EUR':
                text += f"{course['CcyNm_EN']} ----- {course['Rate']} soum"
        await message.answer(text)
    elif message.text == "RUB":
        text = "RUB -----> UZS\n"
        for course in respone:
            if course["Ccy"] == 'RUB':
                text += f"{course['CcyNm_EN']} ----- {course['Rate']} soum"
        await message.answer(text)
    elif message.text == "Other":
        for course in respone:
            text = f"""
{course['Ccy']} -----> UZS
{course['CcyNm_EN']} ----- {course['Rate']} soum"""
            await message.answer(text)
    elif message.text == "Back":
        await message.answer("Choose", reply_markup=english_menu_markup)
        await state.finish()

@dp.message_handler(text="Change the language")
async def ru_change_languag_handler(message: Message):
    await message.answer("Change the language", reply_markup=language_markup)
    await ChangeLanguage.english.set()

@dp.message_handler(state=ChangeLanguage.english)
async def change_language_ru_handler(message: Message, state: FSMContext):
    if message.text == "🇺🇿 O'zbekcha":
        update_language(message.chat.id, "UZ")
        await message.answer("Siz o'zbekchani tanladingiz", reply_markup=uzbek_menu_markup)
    elif message.text == "🇷🇺 Русский":
        update_language(message.chat.id, "RU")
        await message.answer("Вы выбрали узбекский", reply_markup=russian_menu_markup)
    elif message.text == "🇺🇸 English":
        update_language(message.chat.id, "EN")
        await message.answer("You have chosen Uzbek", reply_markup=english_menu_markup)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)