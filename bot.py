import os
import logging
import typing
import re
import json

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types, filters


load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


f = open("files/data.json")
information = json.load(f)
f.close()


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


def contacts_keyboard():
    
    buttons = [
        types.InlineKeyboardButton(text="Единый Деканат", callback_data="contact_dean_office"),
        types.InlineKeyboardButton(text="Главный корпус", callback_data="contact_main_building"),
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



#Stikers handler

@dp.message_handler(content_types=["sticker"])
async def send_welcome(message: types.Message):

    await message.answer_sticker(sticker="https://raw.githubusercontent.com/TelegramBots/book/master/src/docs/sticker-fred.webp")


#Main commands

@dp.message_handler(commands="help")
async def send_welcome(message: types.Message):

    await message.answer(information["RU"]["help"])


@dp.message_handler(commands="start")
async def start_command(message: types.Message):

    await message.answer("Какую информацию вы хотите получить?", reply_markup=start_keyboard())


@dp.message_handler(commands="map")
async def send_contacts(message: types.Message):
    
    media = types.InputFile("files/map.jpg")
    await message.answer_photo(media)


#Callbacks

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
    
    await call.message.edit_text("Какую информацию вы хотите получить?", reply_markup=contacts_keyboard())
    await call.answer()


@dp.callback_query_handler(filters.Regexp(r'ulk-\d+'))
async def send_contacts(call: types.CallbackQuery):
    
    await call.message.edit_text(information["RU"]["campus"][call.data], reply_markup=go_back_keyboard("campus"), disable_web_page_preview=True)
    await call.answer()


@dp.callback_query_handler(filters.Regexp(r'contact_[a-z,A-Z]+'))
async def send_contacts(call: types.CallbackQuery):
    
    await call.message.edit_text(information["RU"]["contacts"][call.data], reply_markup=go_back_keyboard("contacts"), disable_web_page_preview=True)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
