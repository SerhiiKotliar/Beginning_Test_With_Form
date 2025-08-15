import sys
import os
import tkinter as tk
from tkinter import messagebox
import string
import re
from urllib.parse import urlparse


# --- проверки целых значений (для validatecommand с %P) ---
def allow_login_value(new_value: str) -> bool:
    # допускаем пустое (что бы можно было стирать)
    return bool(re.fullmatch(r"[A-Za-z0-9]*", new_value or ""))

def allow_password_value(new_value: str) -> bool:
    # только печатаемые ASCII, без пробела
    return all(32 <= ord(c) <= 126 and c != " " for c in (new_value or ""))


# --- проверки при нажатии OK ---
def validate_password_rules(pw: str):
    if not pw:
        return "Пароль не може бути порожнім."
    if not any(c.islower() for c in pw):
        return "Пароль має містити принаймні одну маленьку літеру."
    if not any(c.isupper() for c in pw):
        return "Пароль має містити принаймні одну велику літеру."
    if not any(c.isdigit() for c in pw):
        return "Пароль має містити принаймні одну цифру."
    if not any(c in string.punctuation for c in pw):
        return "Пароль має містити принаймні один спеціальний символ."
    return None

def validate_url_value(url: str):
    try:
        u = urlparse(url)
        if u.scheme and u.netloc:
            return None
        return "Неправильний формат URL. Приклад: https://example.com"
    except Exception:
        return "Неправильний формат URL."


class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Введення тестових даних")
        self.attributes("-topmost", True)

        self.required_vars = {}
        self.labels = {}
        self.entries = {}
        self.password_visible = False

        # (лейбл, имя_атрибута, дефолт, функция_допустимого_ввода)
        fields = (
            ("Логін:", "login", "", allow_login_value),
            ("Пароль:", "password", "", allow_password_value),
            ("Адреса (URL):", "url", "https://en.wikipedia.org/wiki/Main_Page", None),
        )

        for row, (label_text, attr_name, default, allow_func) in enumerate(fields):
            tk.Label(self, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            self.labels[attr_name] = label_text

            show_char = "*" if attr_name == "password" else ""
            entry = tk.Entry(self, show=show_char)
            entry.insert(0, default)
            entry.config(highlightthickness=1, highlightbackground="gray", highlightcolor="gray")

            # валидация на лету, учитывает вставку (используем %P = proposed value)
            if allow_func is not None:
                vcmd = self._vcmd_factory(entry, allow_func)
                entry.config(validate="key", validatecommand=vcmd)

            entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
            setattr(self, attr_name, entry)
            self.entries[attr_name] = entry

            # чекбокс "Обов'язкове" для каждого поля
            var = tk.BooleanVar(value=True if attr_name in ("login", "password", "url") else False)
            chk = tk.Checkbutton(self, text="Обов'язкове", variable=var)
            chk.grid(row=row, column=2, padx=5, pady=5, sticky="w")
            self.required_vars[attr_name] = var

            # кнопка показать/скрыть рядом только с паролем
            if attr_name == "password":
                btn = tk.Button(self, text="Показати", command=self.toggle_password)
                btn.grid(row=row, column=3, padx=5, pady=5, sticky="w")
                self.show_btn = btn  # сохраним ссылку

        # кнопки управления
        self.submit_button = tk.Button(self, text="OK", command=self.on_ok)
        self.submit_button.grid(row=len(fields), column=0, columnspan=1, pady=10, sticky="we", padx=5)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=len(fields), column=1, columnspan=1, pady=10, sticky="we", padx=5)

        self.bind("<Return>", lambda e: self.on_ok())
        self.result = None
        self.columnconfigure(1, weight=1)  # растягиваем колонку с вводом

        # динамический размер и центрирование
        self.update_idletasks()
        req_width = 600
        req_height = self.winfo_reqheight() + 20
        self.center_window(req_width, req_height)

        # курсор/фокус в конец поля пароля
        self.password.icursor(tk.END)
        self.password.focus_set()

    # ------ helpers ------
    def _vcmd_factory(self, entry, allow_func):
        def _vcmd(new_value):
            ok = allow_func(new_value)
            if ok:
                self._set_ok(entry)
            else:
                self._set_err(entry)
            return ok
        return (self.register(_vcmd), "%P")

    def _set_err(self, entry):
        entry.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")

    def _set_ok(self, entry):
        entry.config(highlightthickness=1, highlightbackground="gray", highlightcolor="gray")

    def center_window(self, width, height):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ------ UI actions ------
    def toggle_password(self):
        if self.password_visible:
            self.password.config(show="*")
            self.show_btn.config(text="Показати")
            self.password_visible = False
        else:
            self.password.config(show="")
            self.show_btn.config(text="Сховати")
            self.password_visible = True

    def on_ok(self):
        # проверяем заполнение обязательных
        missing = []
        for name, var in self.required_vars.items():
            if var.get() and not getattr(self, name).get().strip():
                missing.append(self.labels[name])
                self._set_err(self.entries[name])
            else:
                self._set_ok(self.entries[name])
        if missing:
            messagebox.showerror(
                "Помилка",
                "Будь ласка, заповніть обов'язкові поля зі списку:\n" + "\n".join(missing),
                parent=self
            )
            return

        # предметные проверки
        login_val = self.login.get()
        if not allow_login_value(login_val):
            self._set_err(self.login)
            messagebox.showerror("Помилка", "Логін може містити лише англійські літери та цифри.", parent=self)
            self.login.focus_set()
            return

        pw = self.password.get()
        if not allow_password_value(pw) or (err := validate_password_rules(pw)):
            self._set_err(self.password)
            messagebox.showerror("Помилка", err or "Пароль містить недопустимі символи.", parent=self)
            self.password.focus_set()
            return
        self._set_ok(self.password)

        url_val = self.url.get()
        if (err := validate_url_value(url_val)):
            self._set_err(self.url)
            messagebox.showerror("Помилка", err, parent=self)
            self.url.focus_set()
            return
        self._set_ok(self.url)

        # всё ок
        self.result = {"login": login_val, "password": pw, "url": url_val}
        self.destroy()

    def on_cancel(self):
        self.result = None
        try:
            self.destroy()
            self.update_idletasks()
        finally:
            # полный выход (в т.ч. под pytest)
            os._exit(0)


# вызов диалога
def get_user_input():
    root = tk.Tk()
    root.withdraw()
    dlg = InputDialog(root)
    dlg.grab_set()
    root.wait_window(dlg)
    return dlg.result



# Виклик форми
# user_data = get_user_input()
# print(user_data)
# @pytest.fixture(scope="session")
# def user_data():
#     """Фікстура, яка перед запуском тестів показує форму і повертає введені дані"""
#     # return open_form()
#     return get_user_input()
