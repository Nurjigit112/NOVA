import os
import subprocess
import psutil
import shutil
from typing import List
import ctypes

try:
    from PIL import ImageGrab
except Exception:  # pillow may be missing
    ImageGrab = None


def run_program(path):
    """Запуск внешней программы"""
    try:
        subprocess.Popen(path)
        return True
    except Exception as e:
        print(f"Ошибка запуска {path}: {e}")
        return False


def kill_process(name):
    """Завершение процесса по имени"""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and name.lower() in proc.info['name'].lower():
            psutil.Process(proc.info['pid']).terminate()
            return True
    return False


def system_shutdown():
    os.system("shutdown /s /t 0")


def system_restart():
    os.system("shutdown /r /t 0")


def system_lock():
    if os.name == 'nt':
        os.system("rundll32.exe user32.dll,LockWorkStation")


def execute_shell(command, powershell=False):
    shell = ['powershell', '-Command'] if powershell else ['cmd', '/c']
    try:
        result = subprocess.run(shell + [command], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)


def list_processes():
    """Возвращает список работающих процессов"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append(f"{proc.info['pid']} - {proc.info['name']}")
    return processes


def volume_up():
    """Увеличивает громкость."""
    if os.name == 'nt':
        APPCOMMAND_VOLUME_UP = 0x0a0000
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.SendMessageW(hwnd, 0x319, 0, APPCOMMAND_VOLUME_UP)
    else:
        os.system("pactl set-sink-volume @DEFAULT_SINK@ +5%")


def volume_down():
    """Уменьшает громкость."""
    if os.name == 'nt':
        APPCOMMAND_VOLUME_DOWN = 0x090000
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.SendMessageW(hwnd, 0x319, 0, APPCOMMAND_VOLUME_DOWN)
    else:
        os.system("pactl set-sink-volume @DEFAULT_SINK@ -5%")


def volume_mute():
    """Переключает режим без звука."""
    if os.name == 'nt':
        APPCOMMAND_VOLUME_MUTE = 0x080000
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.SendMessageW(hwnd, 0x319, 0, APPCOMMAND_VOLUME_MUTE)
    else:
        os.system("pactl set-sink-mute @DEFAULT_SINK@ toggle")


def search_files(keyword: str, path: str = '.') -> List[str]:
    """Поиск файлов по ключевому слову."""
    results = []
    for root, _, files in os.walk(path):
        for name in files:
            if keyword.lower() in name.lower():
                results.append(os.path.join(root, name))
    return results


def copy_file(src: str, dst: str) -> None:
    shutil.copy2(src, dst)


def delete_file(path: str) -> None:
    os.remove(path)


def rename_file(src: str, dst: str) -> None:
    os.rename(src, dst)


def take_screenshot(path: str = 'screenshot.png') -> str:
    """Делает скриншот экрана и сохраняет его."""
    if ImageGrab is None:
        raise RuntimeError('Pillow не установлен')
    img = ImageGrab.grab()
    img.save(path)
    return path
