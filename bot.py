import os
import logging
import typing
import re

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types, filters


# Load API key from .env file
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


information = {

    "help": 
"""
Бот-помощник для студентов.

Этот бот создан для помощи студентам ТюмГу в координации внутри университета.

Список команд:
/start  - Запуск бота
/map    - Вывод карты ТюмГу 
""",

    "contacts":
    """
Контакты:
Единый деканат
    """,
    
    "ulk-1": 
"""
🏢УЛК-01 (ИФиЖ)
Адрес: Ул. Республики, 9

Институт социально-гуманитарных наук
Телефон: 59-74-39
Группа ВК: https://vk.com/csi_ipip
""",

    "ulk-3":
"""
🏢УЛК-03 (ИнЗем)
Адрес: Ул. Осипенко, 2

Институт наук о Земле
Телефон: 59-74-91
Группа ВК: https://vk.com/inzemutmn
""",

"ulk-4":
"""
🏢УЛК-04 (ФЭИ)
Адрес: Ул. Ленина, 16

Финансово-экономический институт
Телефон: 59-74-97
Группа ВК: https://vk.com/fei_media
""",

"ulk-5":
"""
🏢УЛК-05 (ИнХим/ФТИ/ИМиКН)
Адрес: Ул. Перекопская, 15а

Институт химии
Телефон: 59-74-67 


Физико-технический институт
Телефон: 59-74-70 
Группа ВК: https://vk.com/ifikh


Институт математики и компьютерных наук
Телефон: 59-77-40
Группа ВК: https://vk.com/utmn_imikn
""",

"ulk-6":
"""
🏢УЛК-06 (ИнБио)
Адрес: Ул. Пирогова, 3

Институт биологии
Телефон: 59-74-94
Группа ВК: https://vk.com/utmn_inbio
""",

"ulk-7":
"""
🏢УЛК-07 (ИФК)
Адрес: Ул. Пржевальского, 37

Институт физической культуры.
СК-спортивный корпус.(корпус-1,2) 
Телефоны: 41-38-88, 41-80-16
Группа ВК: https://vk.com/ifk.utmn
""",

"ulk-9":
"""
🏢УЛК-09
Адресс: Ул. Ленина, 6

Спортивный оздоровительный корпус
""",

"ulk-10":
"""
🏢УЛК-10 (ИГиП)
Адресс: Ул. Ленина, 38

Институт государства и права
Телефон: 59-74-43
Группа ВК: https://vk.com/igipgip

🏢УЛК-10/Т9
Адресс: ул. Тургенева,9

🏢УЛК-10/Р18
Адресс: ул. Республики,18
""",

"ulk-11":
"""
🏢УЛК-11 (СоцГум)
Адресс: Ул. Ленина, 23

Институт дистанционного образования

Институт социально-гуманитарных наук
Телефон: 59-76-79
https://vk.com/socgum_utmn
""",

"ulk-12":
"""
🏢УЛК-12
Адресс: Ул. Семакова, 18

Библиотечно–музейный комплекс
Телефон: 45-63-09
""",

"ulk-13":
"""
🏢УЛК-13
Адресс: Ул. Барнаульская, 4

ЦВЗС Центр зимних видов спорта
Телефон: 43-45-62
""",

"ulk-16":
"""
🏢УЛК-16 (ИПип)
Адресс: Ул. Проезд 9 Мая, 5

Институт психологии и педагогики
Телефон: 59-75-81
Группа ВК: https://vk.com/csi_ipip
""",

"ulk-17":
"""
🏢УЛК-17 (X-BIO)
Адресс: Ул. Володарского 6

Институт экологической и сельскохозяйственной биологии
Телефон: 59-74-00
""", 

"ulk-19":
"""
🏢УЛК-19 (ШПИ)
Адресс: Ул. 8 марта 2/1

Школа перспективных исследований
Телефон: 59-76-58

Политехническая школа
Телефон: 59-74-00
"""
}


def start_keyboard():
    
    buttons = [
        types.InlineKeyboardButton(text="Корпуса", callback_data="campus"),
        types.InlineKeyboardButton(text="Контакты" , callback_data="contacts")
    ]
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    
    return keyboard


def campus_keyboard():
    
    buttons = [
        types.InlineKeyboardButton(text="УЛК-1", callback_data="ulk-1"),
        types.InlineKeyboardButton(text="УЛК-3", callback_data="ulk-3"),
        types.InlineKeyboardButton(text="УЛК-4", callback_data="ulk-4"),
        types.InlineKeyboardButton(text="УЛК-5", callback_data="ulk-5"),
        types.InlineKeyboardButton(text="УЛК-6", callback_data="ulk-6"),
        types.InlineKeyboardButton(text="УЛК-7", callback_data="ulk-7"),
        types.InlineKeyboardButton(text="УЛК-9", callback_data="ulk-9"),
        types.InlineKeyboardButton(text="УЛК-10", callback_data="ulk-10"),
        types.InlineKeyboardButton(text="УЛК-11", callback_data="ulk-11"),
        types.InlineKeyboardButton(text="УЛК-12", callback_data="ulk-12"),
        types.InlineKeyboardButton(text="УЛК-13", callback_data="ulk-13"),
        types.InlineKeyboardButton(text="УЛК-16", callback_data="ulk-16"),
        types.InlineKeyboardButton(text="УЛК-17", callback_data="ulk-17"),
        types.InlineKeyboardButton(text="УЛК-19", callback_data="ulk-19"),
        types.InlineKeyboardButton(text="Назад", callback_data="start_menu")
    ]
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def go_back_keyboard(point):
    
    button = types.InlineKeyboardButton(text="Назад", callback_data=point)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)
    
    return keyboard


@dp.message_handler(commands="help")
async def send_welcome(message: types.Message):

    await message.answer(information["help"])


@dp.message_handler(content_types=["sticker"])
async def send_welcome(message: types.Message):

    await message.answer_sticker(sticker="https://raw.githubusercontent.com/TelegramBots/book/master/src/docs/sticker-fred.webp")


@dp.message_handler(commands="start")
async def start_command(message: types.Message):

    await message.answer("Какую информацию вы хотите получить?", reply_markup=start_keyboard())


@dp.callback_query_handler(text="start_menu")
async def start_menu(call: types.CallbackQuery):

    await call.message.edit_text("Какую информацию вы хотите получить?", reply_markup=start_keyboard())
    await call.answer()


@dp.callback_query_handler(text="campus")
async def send_campus_buttons(call: types.CallbackQuery):

    await call.message.edit_text("Выберите корпус", reply_markup=campus_keyboard())
    await call.answer()


@dp.callback_query_handler(text="contacts")
async def send_contacts(call: types.CallbackQuery):
    
    await call.message.edit_text(information["contacts"], reply_markup=go_back_keyboard("start_menu"))
    await call.answer()


@dp.message_handler(commands="map")
async def send_contacts(message: types.Message):
    
    media = types.InputFile("files/map.jpg")
    await message.answer_photo(media)


@dp.callback_query_handler(filters.Regexp(r'ulk-\d+'))
async def send_contacts(call: types.CallbackQuery):
    
    await call.message.edit_text(information[call.data], reply_markup=go_back_keyboard("campus"), disable_web_page_preview=True)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
