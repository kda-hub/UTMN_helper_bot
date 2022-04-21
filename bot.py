import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types


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
/start - запуск бота
""",

    "contacts":
    """
Контакты:
Единый деканат
что-то
    """,
    
    "ulk-1": 
f"""
УЛК-01 (ИФиЖ)

Институт социально-гуманитарных наук
Адрес: Ул. Республики, 9
Телефон: 59-74-39.
Группа ВК: https://vk.com/csi_ipip
""",

    "ulk-3":
f"""
УЛК-03 (ИнЗем)

Институт наук о Земле
Адрес: Ул. Осипенко, 2
Телефон: 59-74-91
Группа ВК: https://vk.com/inzemutmn
""",
"ulk-4":
"""
УЛК-04 (ФЭИ)

Финансово-экономический институт
Адрес: Ул. Ленина, 16
Телефон: 59-74-97
Группа ВК: https://vk.com/fei_media
""",

"ulk-5":
"""
УЛК-05 (ИнХим/ФТИ/ИМиКН)
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
        types.InlineKeyboardButton(text="УЛК-1", callback_data="ulk_1"),
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


@dp.callback_query_handler(text="ulk_1")
async def send_contacts(call: types.CallbackQuery):
    
    await call.message.edit_text(information["ulk-1"], reply_markup=go_back_keyboard("campus"), disable_web_page_preview=True)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)