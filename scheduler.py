import schedule
import threading
import time
from tts import say


def add_reminder(time_str: str, text: str) -> None:
    """Добавляет ежедневное напоминание."""
    schedule.every().day.at(time_str).do(lambda: say(text))


def run_scheduler() -> None:
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    add_reminder("12:00", "Обед")
    threading.Thread(target=run_scheduler, daemon=True).start()
    while True:
        time.sleep(1)
