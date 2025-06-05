"""Главный модуль запуска ассистента"""
import argparse
import threading
from voice_recognition import listen_command
from gui import build_gui
from telegram_bot import run_bot
from tts import say
from learning import init_db
import assistant_core
import scheduler


def main():
    parser = argparse.ArgumentParser(description='Ассистент Нова')
    parser.add_argument('--nogui', action='store_true', help='Запуск без графического интерфейса')
    parser.add_argument('--bot', action='store_true', help='Запуск Telegram-бота')
    args = parser.parse_args()

    init_db()
    threading.Thread(target=scheduler.run_scheduler, daemon=True).start()

    if args.bot:
        run_bot()
        return

    if args.nogui:
        while True:
            cmd = listen_command()
            if cmd:
                result = assistant_core.process_command(cmd)
                print(result)
                say(result)
    else:
        build_gui()


if __name__ == '__main__':
    main()
