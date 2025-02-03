from data_manager import DataManager
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from dotenv import load_dotenv
from bot import *

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TOKEN_BOT_API_TEST")

datamanager = DataManager()

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("data", work_with_data))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                               lambda update, context: handle_message(update, context, datamanager)))

app.add_handler(CallbackQueryHandler(button_handler))

app.add_handler(MessageHandler(filters.COMMAND, unknown))

app.run_polling()