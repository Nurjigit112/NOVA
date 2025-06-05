import requests

VERSION_URL = 'https://example.com/nova/version'


def check_update(current_version):
    try:
        data = requests.get(VERSION_URL, timeout=5).json()
        latest = data.get('version', current_version)
        if latest != current_version:
            return f'Доступна новая версия {latest}'
        return 'Обновлений нет'
    except Exception:
        return 'Не удалось проверить обновления'
