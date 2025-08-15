import sys
import os
import tkinter as tk
from tkinter import messagebox
import string
import re
from urllib.parse import urlparse


# --- проверки значений ---
def allow_login_value(new_value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9]*", new_value or ""))

def allow_password_value(new_value: str) -> bool:
    return all(32 <= ord(c) <= 126 and c != " " for c in (new_value or ""))

def allow_url_value(new_value: str) -> bool:
    # простая проверка: начинается с http/https и есть хотя бы один "."
    return bool(re.fullmatch(r"https?://[^\s/$.?#].[^\s]*", new_value or ""))


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


# --- Конфиг полей ---
FIELDS_CONFIG = [
    {"label": "Логін:", "name": "login", "default": "", "allow_func": allow_login_value},
    {"label": "Пароль:", "name": "password", "default": "", "allow_func": allow_password_value},
    {"label": "Адреса (URL):", "name": "url", "default": "https://en.wikipedia.org/wiki/Main_Page", "allow_func": allow_url_value},
]


class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Введення тестових даних")
        self.attributes("-topmost", True)

        self.required_vars = {}
        self.labels = {}
        self.entries = {}
        self.password_visible = False

        for row, field in enumerate(FIELDS_CONFIG):
            label_text = field["label"]
            attr_name = field["name"]
            default = field["default"]
            allow_func = field["allow_func"]

            tk.Label(self, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            self.labels[attr_name] = label_text

            show_char = "*" if attr_name == "password" else ""
            entry = tk.Entry(self, show=show_char)
            entry.insert(0, default)
            entry.config(highlightthickness=1, highlightbackground="gray", highlightcolor="gray")

            if allow_func is not None:
                vcmd = self._vcmd_factory(entry, allow_func)
                entry.config(validate="key", validatecommand=vcmd)

            entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
            setattr(self, attr_name, entry)
            self.entries[attr_name] = entry

            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(self, text="Обов'язкове", variable=var)
            chk.grid(row=row, column=2, padx=5, pady=5, sticky="w")
            self.required_vars[attr_name] = var

            if attr_name == "password":
                btn = tk.Button(self, text="Показати", command=self.toggle_password)
                btn.grid(row=row, column=3, padx=5, pady=5, sticky="w")
                self.show_btn = btn

        # кнопки управления
        self.submit_button = tk.Button(self, text="OK", command=self.on_ok)
        self.submit_button.grid(row=len(FIELDS_CONFIG), column=0, columnspan=1, pady=10, sticky="we", padx=5)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=len(FIELDS_CONFIG), column=1, columnspan=1, pady=10, sticky="we", padx=5)

        self.bind("<Return>", lambda e: self.on_ok())
        self.result = None
        self.columnconfigure(1, weight=1)

        self.update_idletasks()
        req_width = 600
        req_height = self.winfo_reqheight() + 20
        self.center_window(req_width, req_height)

        # фокус на первом поле (логин)
        first_field_name = FIELDS_CONFIG[0]["name"]
        self.entries[first_field_name].icursor(tk.END)
        self.entries[first_field_name].focus_set()

    # ------ helpers ------
    def _vcmd_factory(self, entry, allow_func):
        def _vcmd(new_value):
            ok = allow_func(new_value)
            if ok:
                self._set_ok(entry)
            else:
                self._set_err(entry)
            return True  # возвращаем True, чтобы не блокировать ввод
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
                "Будь ласка, заповніть обов'язкові поля:\n" + "\n".join(missing),
                parent=self
            )
            return

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

        self.result = {"login": login_val, "password": pw, "url": url_val}
        self.destroy()

        def on_cancel(self):
            self.result = None
            try:
                self.destroy()
                self.update_idletasks()
            finally:
                os._exit(0)

    # вызов диалога
    def get_user_input():
        root = tk.Tk()
        root.withdraw()
        dlg = InputDialog(root)
        dlg.grab_set()
        root.wait_window(dlg)
        return dlg.result