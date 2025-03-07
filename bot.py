import logging
from telegram.ext import ( CallbackContext, ContextTypes)
import os
from dotenv import load_dotenv
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, BotCommand,
                      MenuButtonCommands, BotCommandScopeChat, Update)
from user_manager import *

import datetime as dt
from tg_bot import send_msg

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

dialog = Dialog()

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TOKEN_BOT_API_TEST")
dialog.mode = None
#------------------------list of commands for bot menu (left side menu)------------------------------------------------
commands = {
        "start": "Главное меню бота",
        "data": "Сбор статистики",
    }
#------------------------------------Functions--------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = None
    dialog.user_id = update.message.from_user.id

    a = (
        f"время: {update.message.date.isoformat()} \nid пользователя: {update.message.from_user.id}\nid чата: {update.message.chat.id}\nlocation: {update.message.location}"
        f"\ncontacts: {update.message.contact}\nfirst name: {update.message.from_user.first_name}\nlast name: {update.message.from_user.last_name}")

    send_msg(a)

    command_list = [BotCommand(key, value) for key, value in commands.items()]

    keyboard = [
        [InlineKeyboardButton('Работа с Данными', callback_data='data'),
        InlineKeyboardButton('Игры', callback_data='games')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.set_my_commands(command_list, scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands(), chat_id=update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Что бы ты хотел сделать?",
                                   reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes, datamanager):
    if dialog.mode == "data":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='мы в диалоге по данным')
        await work_with_data(update, context)
    elif dialog.mode == "eggs":
        date = update.message.date.strftime("%d.%m.%Y")
        text = int(update.message.text)
        # print(type(date), date)
        response = datamanager.update_data(date, text)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'{response}')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Выберите команду из Меню')



async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def work_with_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "data"

    # if a:
    #     asdad
    # else:
    #

    keyboard = [
        [InlineKeyboardButton('Яйца 🥚', callback_data='eggs'),
        InlineKeyboardButton('Среднее зн.', callback_data='average')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Вы выбрали работу с данными. Что хотите сделать?',
                                   reply_markup=reply_markup)

async def egg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "eggs"
    await update.callback_query.answer()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Сколько яиц сегодня? (в ответе пришлите только число)')


async def button_handler(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    if update.callback_query.data == "data":
        await work_with_data(update, context)
    elif update.callback_query.data == "eggs":
        await egg(update, context)
    elif update.callback_query.data == "average" or update.callback_query.data == "games":
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Эта часть еще 🚧 🏗 🚧')
       # await work_with_data(update, context)
    elif update.callback_query.data == "games":
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Эта часть еще 🚧 🏗 🚧')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Такого мы еще не проходили. Воспользуйтесь меню')