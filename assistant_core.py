from system_control import (
    execute_shell,
    run_program,
    kill_process,
    system_shutdown,
    system_restart,
    system_lock,
    volume_up,
    volume_down,
    volume_mute,
    list_processes,
    search_files,
    copy_file,
    delete_file,
    rename_file,
    take_screenshot,
)
from tts import say
from learning import store_interaction, add_custom_command, get_custom_response
import scheduler


def process_command(command: str) -> str:
    """Обрабатывает пользовательскую команду."""
    if not command:
        return ""
    text = command.strip().lower()
    if text.startswith("запомни"):
        parts = text[len("запомни"):].strip().split("=", 1)
        if len(parts) == 2:
            add_custom_command(parts[0].strip(), parts[1].strip())
            response = "Запомнила"
            store_interaction(text, response)
            return response
    if text.startswith("напомни"):
        parts = text[len("напомни"):].strip().split(" ", 1)
        if len(parts) == 2:
            scheduler.add_reminder(parts[0], parts[1])
            response = "Напоминание добавлено"
            store_interaction(text, response)
            return response
    if text.startswith("запусти "):
        path = text[len("запусти "):].strip()
        ok = run_program(path)
        response = f"Запускаю {path}" if ok else f"Не удалось запустить {path}"
        store_interaction(text, response)
        return response

    if text.startswith("закрой процесс "):
        name = text[len("закрой процесс "):].strip()
        ok = kill_process(name)
        response = (
            f"Процесс {name} завершён" if ok else f"Не удалось завершить {name}"
        )
        store_interaction(text, response)
        return response

    if text in ("выключи компьютер", "выключи систему"):
        system_shutdown()
        response = "Выключаю компьютер"
        store_interaction(text, response)
        return response

    if text in ("перезагрузи компьютер", "перезагрузи систему"):
        system_restart()
        response = "Перезагружаю компьютер"
        store_interaction(text, response)
        return response

    if text == "заблокируй компьютер":
        system_lock()
        response = "Компьютер заблокирован"
        store_interaction(text, response)
        return response

    if text in ("громкость плюс", "увеличь громкость"):
        volume_up()
        response = "Громкость увеличена"
        store_interaction(text, response)
        return response

    if text in ("громкость минус", "уменьши громкость"):
        volume_down()
        response = "Громкость уменьшена"
        store_interaction(text, response)
        return response

    if text in ("выключи звук", "звук выкл"):
        volume_mute()
        response = "Звук отключён"
        store_interaction(text, response)
        return response

    if text == "список процессов":
        response = "\n".join(list_processes())
        store_interaction(text, response)
        return response

    if text.startswith("найди файл "):
        keyword = text[len("найди файл "):].strip()
        files = search_files(keyword)
        response = "\n".join(files) if files else "Файлы не найдены"
        store_interaction(text, response)
        return response

    if text.startswith("скопируй файл "):
        parts = text[len("скопируй файл "):].split(" ")
        if len(parts) >= 2:
            src, dst = parts[0], parts[1]
            try:
                copy_file(src, dst)
                response = "Файл скопирован"
            except Exception as e:
                response = f"Ошибка копирования: {e}"
            store_interaction(text, response)
            return response

    if text.startswith("удали файл "):
        path = text[len("удали файл "):].strip()
        try:
            delete_file(path)
            response = "Файл удалён"
        except Exception as e:
            response = f"Ошибка удаления: {e}"
        store_interaction(text, response)
        return response

    if text.startswith("переименуй файл "):
        parts = text[len("переименуй файл "):].split(" ")
        if len(parts) >= 2:
            src, dst = parts[0], parts[1]
            try:
                rename_file(src, dst)
                response = "Файл переименован"
            except Exception as e:
                response = f"Ошибка переименования: {e}"
            store_interaction(text, response)
            return response

    if text == "сделай скриншот":
        try:
            path = take_screenshot()
            response = f"Скриншот сохранён в {path}"
        except Exception as e:
            response = f"Ошибка скриншота: {e}"
        store_interaction(text, response)
        return response

    custom = get_custom_response(text)
    if custom:
        store_interaction(text, custom)
        return custom

    result = execute_shell(text)
    store_interaction(text, result)
    return result


if __name__ == "__main__":
    print(process_command("echo test"))
