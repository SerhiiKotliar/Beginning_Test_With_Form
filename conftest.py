import tkinter as tk
from tkinter import messagebox
import re
import sys

# Конфиг: имя_поля -> (метка, тип_поля, функция_валидации)
FIELDS_CONFIG = [
    ("login", "Логин", "entry", lambda v: re.fullmatch(r"[A-Za-z0-9]+", v) is not None),
    ("password", "Пароль", "password", lambda v: (
        any(c.islower() for c in v) and
        any(c.isupper() for c in v) and
        any(c.isdigit() for c in v) and
        any(c in r"!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for c in v) and
        all(c.isprintable() for c in v)
    )),
    ("url", "URL", "entry", lambda v: re.fullmatch(r"https?://[^\s/$.?#].[^\s]*", v) is not None),
]


class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Введення тестових даних")
        self.attributes('-topmost', True)

        self.entries = {}
        self.result = None

        # Цикл по конфигу
        for i, (field_name, label_text, field_type, _) in enumerate(FIELDS_CONFIG):
            tk.Label(self, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=5)

            entry = tk.Entry(self, show="*" if field_type == "password" else "")
            entry.grid(row=i, column=1, padx=5, pady=5)

            # URL подсветка "на лету"
            if field_name == "url":
                entry.bind("<KeyRelease>", self.validate_url_live)

            self.entries[field_name] = entry

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=len(FIELDS_CONFIG), column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="OK", command=self.on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.on_cancel).pack(side="left", padx=5)

        # Кнопка "Показать пароль"
        for name, label, field_type, _ in FIELDS_CONFIG:
            if field_type == "password":
                tk.Checkbutton(btn_frame, text="Показать пароль",
                               command=lambda e=self.entries[name]: self.toggle_password(e)).pack(side="left", padx=5)

        # Фокус на первом поле
        first_field = list(self.entries.values())[0]
        first_field.focus_set()

        self.bind("<Return>", lambda e: self.on_ok())

    def toggle_password(self, entry):
        if entry.cget("show") == "*":
            entry.config(show="")
        else:
            entry.config(show="*")

    def validate_url_live(self, event):
        url = event.widget.get()
        pattern = r"https?://[^\s/$.?#].[^\s]*"
        if re.fullmatch(pattern, url):
            event.widget.config(bg="lightgreen")
        else:
            event.widget.config(bg="lightcoral")

    def on_ok(self):
        data = {}
        for field_name, label_text, _, validator in FIELDS_CONFIG:
            value = self.entries[field_name].get().strip()
            if not validator(value):
                messagebox.showerror("Ошибка", f"Поле '{label_text}' заполнено неверно!", parent=self)
                return
            data[field_name] = value
        self.result = data
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()
        sys.exit()


def get_user_input():
    root = tk.Tk()
    root.withdraw()
    dialog = InputDialog(root)
    root.wait_window(dialog)
    return dialog.result

#
# if __name__ == "__main__":
#     result = get_user_input()
#     print(result)


# Виклик форми
# user_data = get_user_input()
# print(user_data)
# @pytest.fixture(scope="session")
# def user_data():
#     """Фікстура, яка перед запуском тестів показує форму і повертає введені дані"""
#     # return open_form()
#     return get_user_input()
