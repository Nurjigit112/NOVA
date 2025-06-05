"""Модуль самообучения ассистента с использованием GPT и SQLite"""
import sqlite3
import openai
from typing import Optional

DB_PATH = 'nova.db'


def init_db():
    """Создаёт таблицу взаимодействий при первом запуске."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            response TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def store_interaction(command: str, response: str) -> None:
    """Сохраняет команду и ответ в базе данных."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO interactions (command, response) VALUES (?, ?)",
        (command, response),
    )
    conn.commit()
    conn.close()


def analyze_code(file_path: str) -> str:
    """Отправляет код в GPT и возвращает предложенные улучшения."""
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    prompt = f"Предложи улучшения для следующего кода:\n{code}"
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f'Ошибка обращения к OpenAI API: {e}'
