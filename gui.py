import tkinter as tk
from tkinter import scrolledtext
import threading

from voice_recognition import listen_command
from system_control import execute_shell
from tts import say
from learning import store_interaction

LOG_FILE = 'logs/nova.log'


def append_log(text_widget, message):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')
    text_widget.config(state='normal')
    text_widget.insert(tk.END, message + '\n')
    text_widget.config(state='disabled')
    text_widget.yview(tk.END)


def start_listen(text_widget):
    def worker():
        cmd = listen_command()
        if cmd:
            result = execute_shell(cmd)
            say(result)
            store_interaction(cmd, result)
            append_log(text_widget, f"> {cmd}\n{result}")
    threading.Thread(target=worker, daemon=True).start()


def build_gui():
    root = tk.Tk()
    root.title('Ассистент Нова')

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    log_area = scrolledtext.ScrolledText(frame, width=50, height=15, state='disabled')
    log_area.pack()

    btn_listen = tk.Button(frame, text='Включить микрофон', command=lambda: start_listen(log_area))
    btn_listen.pack(fill='x', pady=5)

    btn_stop = tk.Button(frame, text='Выход', command=root.destroy)
    btn_stop.pack(fill='x', pady=5)

    root.mainloop()


if __name__ == '__main__':
    build_gui()
