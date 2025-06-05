import requests
import json

with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

API_KEY = CONFIG.get('openweather_key', '')


def get_weather(city='Moscow'):
    if not API_KEY:
        return 'Ключ API OpenWeather не настроен'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
    try:
        data = requests.get(url, timeout=5).json()
        if data.get('weather'):
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            return f'Погода в {city}: {desc}, {temp}°C'
        return 'Не удалось получить погоду'
    except Exception as e:
        return f'Ошибка запроса: {e}'


if __name__ == '__main__':
    print(get_weather())
