from system_control import execute_shell
from tts import say
from learning import store_interaction, add_custom_command, get_custom_response
import scheduler


def process_command(command: str) -> str:
    """Обрабатывает пользовательскую команду."""
    if not command:
        return ""
    text = command.strip()
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
    custom = get_custom_response(text)
    if custom:
        store_interaction(text, custom)
        return custom
    result = execute_shell(text)
    store_interaction(text, result)
    return result


if __name__ == "__main__":
    print(process_command("echo test"))
