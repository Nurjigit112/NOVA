import speech_recognition as sr


def listen_command(activation_phrase="нова, включись"):
    """Слушает микрофон и возвращает распознанную команду."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ожидание команды...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Распознано: {text}")
        if activation_phrase.lower() in text.lower():
            return text.lower().replace(activation_phrase.lower(), "").strip()
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")
    return ""
