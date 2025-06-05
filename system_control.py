import os
import subprocess
import psutil


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
