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

    await message.reply("Бот-помошник для студентов")

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
    
    await call.message.edit_text("Контакты", reply_markup=go_back_keyboard("start_menu"))
    await call.answer()


@dp.callback_query_handler(text="ulk_1")
async def send_contacts(call: types.CallbackQuery):
    
    await call.message.edit_text("Улк-1", reply_markup=go_back_keyboard("campus"))
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)