from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import json

from system_control import execute_shell

logging.basicConfig(level=logging.INFO)

with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

TOKEN = CONFIG.get('telegram_token', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я ассистент Нова.')

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = ' '.join(context.args)
    result = execute_shell(cmd)
    await update.message.reply_text(f'Результат:\n{result}')

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Я получил сообщение!')


def run_bot():
    if not TOKEN:
        print('Токен Telegram не задан в config.json')
        return
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('cmd', command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    print('Бот запущен')
    app.run_polling()


if __name__ == '__main__':
    run_bot()
