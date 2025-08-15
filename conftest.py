import tkinter as tk
from tkinter import messagebox
import string
from urllib.parse import urlparse

# -----------------------------
# Функции проверки символов для ввода
# -----------------------------
def only_login_char(char):
    return char.isalnum()

def only_password_char(char):
    return char in string.printable and char != " "

def validate_password(password):
    if not any(c.islower() for c in password):
        return "Пароль має містити принаймні одну маленьку літеру."
    if not any(c.isupper() for c in password):
        return "Пароль має містити принаймні одну велику літеру."
    if not any(c.isdigit() for c in password):
        return "Пароль має містити принаймні одну цифру."
    if not any(c in string.punctuation for c in password):
        return "Пароль має містити принаймні один спеціальний символ."
    return None

def validate_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return None
        else:
            return "Неправильний формат URL. Повинен бути, наприклад, https://example.com"
    except Exception:
        return "Неправильний формат URL."

# -----------------------------
# Класс InputDialog с анимацией подсветки
# -----------------------------
class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Введення тестових даних")
        self.attributes('-topmost', True)

        self.required_vars = {}
        self.labels = {}
        self.entries = {}

        fields = (
            ("Логін:", "login", "", only_login_char),
            ("Пароль:", "password", "", only_password_char),
            ("Адреса (URL):", "url", "", None)
        )

        for row, (label_text, attr_name, default, validate_func) in enumerate(fields):
            lbl = tk.Label(self, text=label_text)
            lbl.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            self.labels[attr_name] = label_text

            entry = tk.Entry(self, show="*" if attr_name == "password" else "")
            entry.insert(0, default)
            entry.config(highlightthickness=1, highlightbackground="gray")

            if validate_func:
                vcmd = (self.register(self._on_validate(validate_func, entry)), '%S')
                entry.config(validate="key", validatecommand=vcmd)

            entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
            setattr(self, attr_name, entry)
            self.entries[attr_name] = entry

            var = tk.BooleanVar()
            chk = tk.Checkbutton(self, text="Обов'язкове", variable=var)
            chk.grid(row=row, column=2, padx=5, pady=5, sticky="w")
            self.required_vars[attr_name] = var

        self.submit_button = tk.Button(self, text="OK", command=self.on_button_click)
        self.submit_button.grid(row=len(fields), column=0, pady=10, sticky="we", padx=5)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=len(fields), column=1, pady=10, sticky="we", padx=5)

        self.bind("<Return>", self.on_button_click)
        self.result = None
        self.columnconfigure(1, weight=1)

        self.update_idletasks()
        req_width = 500
        req_height = self.winfo_reqheight() + 20
        self.center_window(req_width, req_height)

    def _on_validate(self, func, entry_widget):
        """Функция для validatecommand с подсветкой"""
        def wrapper(char):
            if func(char):
                self._animate_valid(entry_widget)
                return True
            else:
                entry_widget.config(highlightthickness=2, highlightbackground="red")
                return False
        return wrapper

    def _animate_valid(self, entry_widget):
        """Плавно возвращает рамку к нормальному виду"""
        current = entry_widget.cget("highlightthickness")
        target = 1
        if current > target:
            entry_widget.config(highlightthickness=current-1)
            self.after(20, lambda: self._animate_valid(entry_widget))
        else:
            entry_widget.config(highlightthickness=1, highlightbackground="gray")

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _highlight_error(self, entry_widget):
        entry_widget.config(highlightthickness=2, highlightbackground="red")

    def on_button_click(self, event=None):
        missing_fields = []
        for name, var in self.required_vars.items():
            if var.get():
                value = getattr(self, name).get().strip()
                if not value:
                    missing_fields.append(self.labels[name])
                    self._highlight_error(self.entries[name])
                else:
                    self._animate_valid(self.entries[name])

        if missing_fields:
            messagebox.showerror(
                "Помилка",
                "Будь ласка, заповніть обов'язкові поля:\n" + "\n".join(missing_fields),
                parent=self
            )
            return

        # Проверка пароля
        password_err = validate_password(self.password.get())
        if password_err:
            messagebox.showerror("Помилка", password_err, parent=self)
            self._highlight_error(self.password)
            self.password.focus_set()
            return
        else:
            self._animate_valid(self.password)

        # Проверка URL
        url_err = validate_url(self.url.get())
        if url_err:
            messagebox.showerror("Помилка", url_err, parent=self)
            self._highlight_error(self.url)
            self.url.focus_set()
            return
        else:
            self._animate_valid(self.url)

        self.result = {
            "login": self.login.get(),
            "password": self.password.get(),
            "url": self.url.get()
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Ховаємо головне вікно
    # Створюємо діалогове вікно
    dialog = InputDialog(root)
    dialog.grab_set()  # Блокує взаємодію з іншими вікнами, поки не закриють діалог
    root.wait_window(dialog)  # Очікує закриття діалогу

    return dialog.result


# Виклик форми
# user_data = get_user_input()
# print(user_data)
# @pytest.fixture(scope="session")
# def user_data():
#     """Фікстура, яка перед запуском тестів показує форму і повертає введені дані"""
#     # return open_form()
#     return get_user_input()
