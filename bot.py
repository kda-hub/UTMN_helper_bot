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
        types.InlineKeyboardButton(text = "1", callback_data="ulk_1")
    ]
    
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard


@dp.message_handler(commands="help")
async def send_welcome(message: types.Message):

    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="start")
async def start_command(message: types.Message):

    keyboard = start_keyboard()

    await message.answer("Какую информацию вы хотите получить?", reply_markup=keyboard)


@dp.callback_query_handler(text="campus")
async def send_campus_buttons(call: types.CallbackQuery):

    await call.message.answer("Выберите корпус", reply_markup=campus_keyboard())
    await call.answer()


@dp.callback_query_handler(text="contacts")
async def send_contacts(call: types.CallbackQuery):
    
    await call.message.answer("Контакты")
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)