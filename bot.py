import os
import logging
import typing
import re
import json
import sqlite3

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types, filters


# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)


# Connect to bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Load data
f = open("files/data.json")
information = json.load(f)
f.close()


# Load and setup database
connection = sqlite3.connect('data.db')

sql_query = '''CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    language TEXT); '''

cursor = connection.cursor()
cursor.execute(sql_query)
connection.commit()

cursor.close()
connection.close()


# Keyboards
def menu_keyboard(language):

    buttons = [
        types.InlineKeyboardButton(text=information[language]["buttons"]["campus"], callback_data="campus"),
        types.InlineKeyboardButton(text=information[language]["buttons"]["contacts"], callback_data="contacts")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def language_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="🇷🇺RU", callback_data = "RU"),
        types.InlineKeyboardButton(text="🇬🇧EN", callback_data = "EN"),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def campus_keyboard():

    buttons = [
        types.InlineKeyboardButton(text="УЛК-1/Building-1", callback_data="ulk-1"),
        types.InlineKeyboardButton(text="УЛК-3/Building-3", callback_data="ulk-3"),
        types.InlineKeyboardButton(text="УЛК-4/Building-4", callback_data="ulk-4"),
        types.InlineKeyboardButton(text="УЛК-5/Building-5", callback_data="ulk-5"),
        types.InlineKeyboardButton(text="УЛК-6/Building-6", callback_data="ulk-6"),
        types.InlineKeyboardButton(text="УЛК-7/Building-7", callback_data="ulk-7"),
        types.InlineKeyboardButton(text="УЛК-9/Building-9", callback_data="ulk-9"),
        types.InlineKeyboardButton(text="УЛК-10/Building-10", callback_data="ulk-10"),
        types.InlineKeyboardButton(text="УЛК-11/Building-11", callback_data="ulk-11"),
        types.InlineKeyboardButton(text="УЛК-12/Building-12", callback_data="ulk-12"),
        types.InlineKeyboardButton(text="УЛК-13/Building-13", callback_data="ulk-13"),
        types.InlineKeyboardButton(text="УЛК-16/Building-16", callback_data="ulk-16"),
        types.InlineKeyboardButton(text="УЛК-17/Building-17", callback_data="ulk-17"),
        types.InlineKeyboardButton(text="УЛК-19/Building-19", callback_data="ulk-19"),

        types.InlineKeyboardButton(text="Назад/Back", callback_data="start_menu")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def contacts_keyboard(language):

    buttons = [
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["deans_office"], callback_data="contact_deans_office"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["main_building"], callback_data="contact_main_building"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["selection_committee"], callback_data="contact_selection_committee"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["documentation_service"], callback_data="contact_documentation_service"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["press_service"], callback_data="contact_press_service"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["advertising_marketing"], callback_data="contact_advertising_marketing"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["accounting_and_finance"], callback_data="contact_accounting_and_finance"),
        types.InlineKeyboardButton(text=information[language]["buttons"]["information_technology_center"],
                                   callback_data="contact_information_technology_center"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["personnel"], callback_data="contact_personnel"),
        types.InlineKeyboardButton(
            text=information[language]["buttons"]["center_olympia"], callback_data="contact_center_olympia"),

        types.InlineKeyboardButton(text=information[language]["buttons"]["back"], callback_data="start_menu")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def go_back_keyboard(point, language):

    button = types.InlineKeyboardButton(text=information[language]["buttons"]["back"], callback_data=point)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)

    return keyboard


# SQL
def setup(user_id, language):

    if not is_exists(user_id=user_id):
        connection = sqlite3.connect('data.db')

        sql_query = """INSERT INTO Users (user_id, language)
            VALUES(?, ?)"""

        cursor = connection.cursor()
        cursor.execute(sql_query, [user_id, language])

        connection.commit()
        cursor.close()
        connection.close()


def update_language(user_id, language):

    if is_exists(user_id=user_id):
        connection = sqlite3.connect('data.db')

        sql_query = """UPDATE Users
        SET language = ?
        WHERE user_id = ?;"""

        cursor = connection.cursor()
        cursor.execute(sql_query, [language, user_id])

        connection.commit()
        cursor.close()
        connection.close()


def is_exists(user_id):

    connection = sqlite3.connect('data.db')
    sql_query = '''SELECT EXISTS(SELECT 1 FROM Users WHERE user_id=?);'''

    cursor = connection.cursor()
    cursor.execute(sql_query, [user_id, ])

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]


def get_language(user_id):

    connection = sqlite3.connect('data.db')
    sql_query = '''SELECT language FROM Users WHERE user_id=?'''

    cursor = connection.cursor()
    cursor.execute(sql_query, [user_id, ])

    result = cursor.fetchone()
    return result[0]


# Stikers handler

@dp.message_handler(content_types=["sticker"])
async def send_welcome(message: types.Message):

    await message.answer_sticker(sticker="https://raw.githubusercontent.com/TelegramBots/book/master/src/docs/sticker-fred.webp")
    

# Main commands

@dp.message_handler(commands="start")
async def start_command(message: types.Message):

    setup(user_id=message.from_user.id, language="RU")

    await message.answer("Бот готов к работе! Для смены языка напишите /lang\nThe bot is ready to work! To change the language, print /lang")


@dp.message_handler(commands="lang")
async def language_command(message: types.Message):

    user_id = message.from_user.id

    if is_exists(user_id=user_id):
        await message.answer(text="Выберите язык / Select a language", reply_markup=language_keyboard())
    else:
        await message.answer("Сначала введите команду /start\nFirst enter the command /start")


@dp.message_handler(commands="help")
async def send_welcome(message: types.Message):

    user_id = message.from_user.id

    if is_exists(user_id=user_id):
        language = get_language(user_id=user_id)
        await message.answer(information[language]["help"])
    else:
        await message.answer("Сначала введите команду /start\nFirst enter the command /start")


@dp.message_handler(commands="menu")
async def menu_command(message: types.Message):

    user_id = message.from_user.id

    if is_exists(user_id=user_id):
        language = get_language(user_id=user_id)

        await message.answer(text=information[language]["buttons"]["find_info"], reply_markup=menu_keyboard(language=language))
    else:
        await message.answer("Сначала введите команду /start\nFirst enter the command /start")


@dp.message_handler(commands="map")
async def send_contacts(message: types.Message):

    media = types.InputFile("files/map.jpg")
    await message.answer_photo(media)


# Callbacks

@dp.callback_query_handler(text="start_menu")
async def start_menu(call: types.CallbackQuery):

    language = get_language(user_id=call.from_user.id)
    await call.message.edit_text(text=information[language]["buttons"]["find_info"], reply_markup=menu_keyboard(language=language))
    await call.answer()


@dp.callback_query_handler(text="RU")
async def select_language_ru(call: types.CallbackQuery):

    update_language(user_id=call.from_user.id, language="RU")
    await call.message.answer(text="Выбран русский язык")
    await call.answer()


@dp.callback_query_handler(text="EN")
async def select_language_ru(call: types.CallbackQuery):

    update_language(user_id=call.from_user.id, language="EN")
    await call.message.answer(text="English is selected")
    await call.answer()


@dp.callback_query_handler(text="campus")
async def send_campus_buttons(call: types.CallbackQuery):

    language = get_language(user_id=call.from_user.id)

    await call.message.edit_text(text=information[language]["buttons"]["select_campus"], reply_markup=campus_keyboard())
    await call.answer()


@dp.callback_query_handler(text="contacts")
async def send_contacts(call: types.CallbackQuery):

    language = get_language(user_id=call.from_user.id)
    await call.message.edit_text(text=information[language]["buttons"]["find_info"], reply_markup=contacts_keyboard(language=language))
    await call.answer()


@dp.callback_query_handler(filters.Regexp(r'ulk-\d+'))
async def send_contacts(call: types.CallbackQuery):

    language = get_language(user_id=call.from_user.id)

    await call.message.edit_text(information[language]["campus"][call.data], reply_markup=go_back_keyboard("campus",language=language), disable_web_page_preview=True)
    await call.answer()


@dp.callback_query_handler(filters.Regexp(r'contact_[a-z,A-Z]+'))
async def send_contacts(call: types.CallbackQuery):

    language = get_language(user_id=call.from_user.id)

    await call.message.edit_text(information[language]["contacts"][call.data], reply_markup=go_back_keyboard("contacts", language=language), disable_web_page_preview=True)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
