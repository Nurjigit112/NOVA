from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import json

import os
import sys
import asyncio
from system_control import system_shutdown, system_restart, system_lock, take_screenshot
from assistant_core import process_command

logging.basicConfig(level=logging.INFO)

with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

TOKEN = CONFIG.get('telegram_token', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я ассистент Нова.')

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = ' '.join(context.args)
    result = process_command(cmd)
    await update.message.reply_text(f'Результат:\n{result}')

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = process_command(update.message.text)
    await update.message.reply_text(result)


async def send_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(open('logs/nova.log', 'rb'))


async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = take_screenshot()
    await update.message.reply_photo(open(path, 'rb'))


async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Выключаю систему')
    system_shutdown()


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Перезагрузка системы')
    system_restart()


async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Блокировка системы')
    system_lock()


async def bot_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот отключается')
    asyncio.get_event_loop().call_later(1, os._exit, 0)


async def bot_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот перезапускается')
    asyncio.get_event_loop().call_later(1, os.execl, sys.executable, sys.executable, *sys.argv)


def run_bot():
    if not TOKEN:
        print('Токен Telegram не задан в config.json')
        return
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('cmd', command))
    app.add_handler(CommandHandler('logs', send_logs))
    app.add_handler(CommandHandler('screenshot', screenshot))
    app.add_handler(CommandHandler('shutdown', shutdown))
    app.add_handler(CommandHandler('restart', restart))
    app.add_handler(CommandHandler('lock', lock))
    app.add_handler(CommandHandler('botoff', bot_off))
    app.add_handler(CommandHandler('botrestart', bot_restart))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    print('Бот запущен')
    app.run_polling()


if __name__ == '__main__':
    run_bot()
