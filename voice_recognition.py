import speech_recognition as sr


def listen_command():
    """Слушает микрофон и возвращает текст без проверки ключевых слов."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ожидание команды...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Распознано: {text}")
        return text.lower().strip()
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")
    return ""
