import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import sys

from voice_recognition import listen_command
import assistant_core

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
            result = assistant_core.process_command(cmd)
            assistant_core.say(result)
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

    def clear_logs(text_widget):
        open(LOG_FILE, 'w').close()
        text_widget.config(state='normal')
        text_widget.delete('1.0', tk.END)
        text_widget.config(state='disabled')

    def restart_app():
        os.execl(sys.executable, sys.executable, *sys.argv)

    btn_clear = tk.Button(frame, text='Очистить логи', command=lambda: clear_logs(log_area))
    btn_clear.pack(fill='x', pady=5)

    btn_restart = tk.Button(frame, text='Перезапуск', command=restart_app)
    btn_restart.pack(fill='x', pady=5)

    btn_stop = tk.Button(frame, text='Выход', command=root.destroy)
    btn_stop.pack(fill='x', pady=5)

    root.mainloop()


if __name__ == '__main__':
    build_gui()
