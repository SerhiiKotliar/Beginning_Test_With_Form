import pytest
import tkinter as tk
from tkinter import messagebox


def open_form():
    """Відкриває графічну форму і повертає введені дані"""
    data = {}

    def submit():
        # Перевірка полів, де чекбокс увімкнений
        if chk_username_var.get() and not entry_username.get().strip():
            messagebox.showerror("Помилка", "Поле Username є обов'язковим!")
            return
        if chk_password_var.get() and not entry_password.get().strip():
            messagebox.showerror("Помилка", "Поле Password є обов'язковим!")
            return
        if chk_url_var.get() and not entry_url.get().strip():
            messagebox.showerror("Помилка", "Поле URL є обов'язковим!")
            return

        data["username"] = entry_username.get()
        data["password"] = entry_password.get()
        data["url"] = entry_url.get()
        root.destroy()

    root = tk.Tk()
    root.title("Введіть дані для тестів")

    # Username
    frame_username = tk.Frame(root)
    frame_username.pack(anchor="w", pady=2)
    tk.Label(frame_username, text="Логін:").pack(side="left")
    entry_username = tk.Entry(frame_username)
    entry_username.pack(side="left")
    chk_username_var = tk.BooleanVar()
    tk.Checkbutton(frame_username, text="Обов'язково", variable=chk_username_var).pack(side="left", padx=5)

    # Password
    frame_password = tk.Frame(root)
    frame_password.pack(anchor="w", pady=2)
    tk.Label(frame_password, text="Пароль:").pack(side="left")
    entry_password = tk.Entry(frame_password, show="*")
    entry_password.pack(side="left")
    chk_password_var = tk.BooleanVar()
    tk.Checkbutton(frame_password, text="Обов'язково", variable=chk_password_var).pack(side="left", padx=5)

    # URL
    frame_url = tk.Frame(root)
    frame_url.pack(anchor="w", pady=2)
    tk.Label(frame_url, text="URL:").pack(side="left")
    entry_url = tk.Entry(frame_url)
    entry_url.pack(side="left")
    chk_url_var = tk.BooleanVar()
    tk.Checkbutton(frame_url, text="Обов'язково", variable=chk_url_var).pack(side="left", padx=5)

    tk.Button(root, text="OK", command=submit).pack(pady=5)

    root.mainloop()
    return data


@pytest.fixture(scope="session")
def user_data():
    """Фікстура, яка перед запуском тестів показує форму і повертає введені дані"""
    return open_form()
