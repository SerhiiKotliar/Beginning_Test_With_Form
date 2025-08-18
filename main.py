import tkinter as tk
from tkinter import messagebox
import re
import string
from urllib.parse import urlparse
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import Qt
from pyside_dialog import MyDialog  # твоя PySide форма
# import sys
import os

email = ""
url = ""
# lenmin = 4
# lenmax = 16
lenminlog = 4
lenmaxlog = 16
lenminpas = 8
lenmaxpas = 20
# local = ""
# both_reg = False
# is_probel = False
latin = "A-Za-z"
cyrylic = "А-Яа-я"
# digits = "0-9"
digits = ""
# spec = "!@#$%^&*()-_=+[]{};:,.<>/?\\|"
spec = ""
spec_escaped = ""
# экранируем спецсимволы
upregcyr = "А-Я"
lowregcyr = "а-я"
upreglat = "A-Z"
lowreglat = "a-z"
# letters = "A-Za-z"
pattern = ""
patternlog: str = ""
patternpas: str = ""
chars = ""

def entries_rules(fname, **kwargs):
    global pattern, chars, len_min, len_max, latin, cyrylic, spec_escaped, is_probel, email, url, both_reg, patternlog, patternpas, lenminpas, lenmaxpas, lenminlog, lenmaxlog

    entries = kwargs["entries"]

    # инициализация переменных
    local = ""
    latin = "A-Za-z"
    cyrylic = "А-Яа-я"
    digits = ""
    spec_escaped = ""
    is_probel = False
    len_min = 0
    len_max = 0
    email = False
    url = False
    both_reg = False

    for key, value in entries.items():
        if key == 'localiz':
            if value == 'латиниця':
                local = latin
            elif value == 'кирилиця':
                local = cyrylic

        elif key == 'register':
            if value == 'великий':
                latin = upreglat
                cyrylic = upregcyr
            elif value == "малий":
                latin = lowreglat
                cyrylic = lowregcyr
            elif value == "обидва":
                both_reg = True

        elif key == "cyfry" and value:
            digits = "0-9"

        elif key == "spec" and value:
            spec = "!@#$%^&*()-_=+[]{};:,.<>/?\\|"
            spec_escaped = "".join(re.escape(ch) for ch in spec)

        elif key == "probel":
            is_probel = value

        elif key == "len_min":
            len_min = value

        elif key == "len_max":
            len_max = value

        elif key == "email_in" and value:
            email = "A-Za-z0-9@._\-"

        elif key == "url_in" and value:
            url = "http?://[^\s/$.?#].[^\s]"

    # собираем разрешённые символы
    parts = []
    if local:
        parts.append(local)
    if spec_escaped:
        parts.append(spec_escaped)
    if digits:
        parts.append(digits)
    if is_probel:
        parts.append('^\s')

    chars = "".join(parts) or "."  # если ничего не выбрано — разрешаем всё
    if email:
        # parts.append(email)
        chars = "A-Za-z0-9@._\-"
    if url:
        # parts.append(url)
        chars ="http?://[^\s/$.?#].[^\s]"
    # финальный паттерн с учётом длины
    # pattern = f"[{chars}]{{{len_min},{len_max}}}"
    pattern = f"[{chars}]*"
    # print("✅ Готовый паттерн:", pattern)
    if fname == "login":
        lenminlog = len_min
        lenmaxlog = len_max
        patternlog = pattern
    if fname == "password":
        lenminpas = len_min
        lenmaxpas = len_max
        patternpas = pattern
    return pattern


# --- проверки при вводе ---
def allow_login_value(new_value: str) -> bool:
    global pattern, chars, patternlog
    if not new_value:
        return True
    # если chars == ".", разрешаем всё
    if chars == ".":
        return True
    # pattern = f"[{chars}]*"
    # patternlog = pattern
    return bool(re.fullmatch(patternlog, new_value))

def allow_password_value(new_value: str) -> bool:
    global pattern, chars, patternpas
    if not new_value:
        return True
    # если chars == ".", разрешаем всё
    if chars == ".":
        return True
    # pattern = f"[{chars}]*"
    # patternpas = pattern
    return bool(re.fullmatch(patternpas, new_value))
    # return len(new_value) <= 20 and all(32 <= ord(c) <= 126 and c != " " for c in (new_value or ""))

def allow_url_value(new_value: str) -> bool:
    # return bool(re.fullmatch(r"http?://[^\s/$.?#].[^\s]*", new_value or ""))
    return bool(re.fullmatch(pattern, new_value or ""))
# --- проверки Email при вводе ---
def allow_email_value(new_value: str) -> bool:
    if not new_value:
        return True
    # простой паттерн для "live" проверки: разрешаем буквы, цифры, @, ., -, _
    # pattern = r"[A-Za-z0-9@._\-]*"
    return bool(re.fullmatch(pattern, new_value))

def validate_email_rules(email: str):
    if not email:
        return "Email не може бути порожнім."
    # RFC 5322 упрощённая проверка
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.fullmatch(pattern, email):
        return "Неправильний формат Email."
    return None

# --- проверки при OK ---
def validate_login_rules(log: str):
    global both_reg, digits, spec_escaped
    if not log :
        return "Логін не може бути порожнім."
    if len(log) < lenminlog or len(log) > lenmaxlog:
        return f"Логін має бути від {lenminlog} до {lenmaxlog} символів включно"
    if both_reg:
        if not any(c.islower() for c in log):
            return "Логін має містити принаймні одну маленьку літеру."
        if not any(c.isupper() for c in log):
            return "Логін має містити принаймні одну велику літеру."
    if digits:
        if not any(c.isdigit() for c in log):
            return "Логін має містити принаймні одну цифру."
    if spec_escaped:
        if not any(c in string.punctuation for c in log):
            return "Логін має містити принаймні один спеціальний символ."
    return None

def validate_password_rules(pw: str):
    global both_reg, digits, spec_escaped
    if not pw:
        return "Пароль не може бути порожнім."
    if len(pw) < lenminpas or len(pw) > lenmaxpas:
        return f"Пароль має бути від {lenminpas} до {lenmaxpas} символів включно"
    if both_reg:
        if not any(c.islower() for c in pw):
            return "Пароль має містити принаймні одну маленьку літеру."
        if not any(c.isupper() for c in pw):
            return "Пароль має містити принаймні одну велику літеру."
    if digits:
        if not any(c.isdigit() for c in pw):
            return "Пароль має містити принаймні одну цифру."
    if spec_escaped:
        if not any(c in string.punctuation for c in pw):
            return "Пароль має містити принаймні один спеціальний символ."
    return None

def validate_url_value(url: str):
    if not url:
        return "URL не може бути порожнім."
    allowed_pattern = re.compile(
        r'^[A-Za-z][A-Za-z0-9+.-]*://'
        r'([A-Za-z0-9\-._~%!$&\'()*+,;=]+@)?'
        r'([A-Za-z0-9\-._~%]+|\[[0-9a-fA-F:.]+\])'
        r'(:[0-9]+)?'
        r'(/[A-Za-z0-9\-._~%!$&\'()*+,;=:@]*)*'
        r'(\?[A-Za-z0-9\-._~%!$&\'()*+,;=:@/?]*)?'
        r'(#[A-Za-z0-9\-._~%!$&\'()*+,;=:@/?]*)?$'
    )
    if not allowed_pattern.fullmatch(url):
        return "URL містить недопустимі символи або неправильний формат."
    try:
        u = urlparse(url)
        if u.scheme not in ("http", "https") or not u.netloc:
            return "URL повинен починатися з http:// або https:// і містити домен."
    except Exception:
        return "Неправильний формат URL."
    return None

# --- конфиг полей ---
FIELDS_CONFIG = [
    {"label": "Логін:", "name": "login", "default": "", "allow_func": allow_login_value},
    {"label": "Пароль:", "name": "password", "default": "", "allow_func": allow_password_value},
    {"label": "Адреса (URL):", "name": "url", "default": "https://en.wikipedia.org/wiki/Main_Page", "allow_func": allow_url_value},
    {"label": "Email:", "name": "email", "default": "", "allow_func": allow_email_value},
]

class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Введення тестових даних")
        self.attributes("-topmost", True)

        self.entries = {}
        self.required_vars = {}
        self.labels = {}

        for row, field in enumerate(FIELDS_CONFIG):
            label_text = field["label"]
            name = field["name"]
            default = field["default"]
            allow_func = field["allow_func"]

            tk.Label(self, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            self.labels[name] = label_text

            entry = tk.Entry(self)
            entry.insert(0, default)
            entry.config(highlightthickness=1, highlightbackground="gray", highlightcolor="gray", state=tk.DISABLED)

            if allow_func:
                vcmd = self._vcmd_factory(entry, allow_func)
                entry.config(validate="key", validatecommand=vcmd)

            entry.grid(row=row, column=1, sticky="we", padx=5, pady=5)
            self.entries[name] = entry
            setattr(self, name, entry)

            if name != "login" and name != "password":
                var = tk.BooleanVar(value=False)
                self.required_vars[name] = False
            else:
                var = tk.BooleanVar(value=True)
                self.required_vars[name] = True
            chk = tk.Checkbutton(self, text="Обов'язкове", variable=var,
        command=lambda name=name, v=var: self.on_toggle(name, v))
            chk.grid(row=row, column=2, sticky="w", padx=5, pady=5)
            # self.required_vars[name] = var

            # кнопка для виклику toggle_rule
            btn = tk.Button(self, text="Правила",
                            command=lambda n=name: self.toggle_rule(n))
            # btn = tk.Button(self, text="Правила", command=self.toggle_rule)
            btn.grid(row=row, column=3, sticky="w", padx=5, pady=5)

        self.submit_button = tk.Button(self, text="OK", command=self.on_ok)
        self.submit_button.grid(row=len(FIELDS_CONFIG), column=0, padx=5, pady=10, sticky="we")

        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=len(FIELDS_CONFIG), column=1, padx=5, pady=10, sticky="we")

        self.columnconfigure(1, weight=1)
        self.result = None

        self.update_idletasks()
        self.center_window(600, self.winfo_reqheight() + 20)

        first_field = FIELDS_CONFIG[0]["name"]
        self.entries[first_field].focus_set()

    def on_toggle(self, name, var):
        # state = "включен" if var.get() else "выключен"
        # # print(f"Чекбокс '{name}' {state}")
        # self.required_vars[name] = var
        if var.get():
            state = "включен"
            self.required_vars[name] = True
        else:
            state = "выключен"
            self.required_vars[name] = False
    # --- validatecommand factory ---
    def _vcmd_factory(self, entry, allow_func):
        def _vcmd(new_value):
            if allow_func(new_value):
                entry.config(highlightthickness=1, highlightbackground="gray", highlightcolor="gray")
            else:
                entry.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")
            return True
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
    # відкриття форми з налаштуваннями тестів
    def toggle_rule(self, field_name):
        global patternl, patternpas, pattern
        for en in self.entries.values():
            if en['state'] == tk.NORMAL:
                en.config(state=tk.DISABLED)
        # print(f"Натиснута кнопка для поля: {field_name}")
        entry = self.entries[field_name]
        entry.config(state=tk.NORMAL)
        entry.focus_set()
        global len_max, len_min, lenminlog, lenmaxlog, lenminpas, lenmaxpas
        app = QApplication.instance()
        if not app:
            app = QApplication([])
        dlg = MyDialog()
        # cur_rules = dlg.result

        # entries_rules({field_name: cur_rules})

        dlg.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        dlg.setModal(True)
        if dlg.exec() == QDialog.Accepted:  # ← проверка, нажата ли OK
            cur_rules = dlg.result  # ← берём результат после закрытия
            entries_rules(field_name, entries=cur_rules)

        # if dlg.chkbSpecS.isChecked():
        #     spec = "!@#$%^&*()-_=+[]{};:,.<>/?\\|"
        #     spec_escaped = "".join(re.escape(ch) for ch in spec)

    def on_ok(self):
        # missing = [name for name, var in self.required_vars.items()
        #            if var.get() and not getattr(self, name).get().strip()]
        # missing = [name for name, var in self.required_vars.items() if var.get()]
        # missing = [name for name, var in self.required_vars.items() if not var.get() and self.entries[name].get()==""]
        missing = [name for name, var in self.required_vars.items() if var and self.entries[name].get()==""]
        for name in missing:
            if not self.entries[name].get():
                self._set_err(self.entries[name])
        if missing:
            messagebox.showerror("Помилка", "Будь ласка, заповніть обов'язкові поля:\n" +
                                 "\n".join(self.labels[n] for n in missing), parent=self)
            return

        login_val = self.login.get()
        if "login" in self.required_vars and login_val !="":
            errlog = validate_login_rules(login_val)
            if not allow_login_value(login_val) or errlog:
                self._set_err(self.login)
                messagebox.showerror("Помилка", errlog or "Логін містить недопустимі символи.", parent=self)
                self.login.focus_set()
                return
            self._set_ok(self.login)

        pw = self.password.get()
        if "password" in self.required_vars and pw != "":
            errp = validate_password_rules(pw)
            if not allow_password_value(pw) or errp:
                self._set_err(self.password)
                messagebox.showerror("Помилка", errp or "Пароль містить недопустимі символи.", parent=self)
                self.password.focus_set()
                return
            self._set_ok(self.password)

        url_val = self.url.get()
        if "url" in self.required_vars and url_val != "":
            erru = validate_url_value(url_val)
            if erru:
                self._set_err(self.url)
                messagebox.showerror("Помилка", erru, parent=self)
                self.url.focus_set()
                return
            self._set_ok(self.url)

# проверка Email
        email_val = self.email.get()
        if "email" in self.required_vars and email_val != "":
            erre = validate_email_rules(email_val)
            if not allow_email_value(email_val) or erre:
                self._set_err(self.email)
                messagebox.showerror("Помилка", erre or "Email містить недопустимі символи.", parent=self)
                self.email.focus_set()
                return
            self._set_ok(self.email)

        self.result = {"login": login_val, "password": pw, "url": url_val, "email": email_val}
        self.destroy()


    def on_cancel(self):
        # self.result = None
        # self.destroy()
        # sys.exit(0)
        # self.result = None
        # # Закрываем все окна Tk
        # try:
        #     self.destroy()  # закрываем текущий диалог
        #     self.master.destroy()  # закрываем главное окно
        # except Exception:
        #     pass
        self.result = None
        try:
            self.destroy()
        finally:
            os._exit(0)  # немедленно завершает процесс

# --- вызов диалога ---
def get_user_input():
    root = tk.Tk()
    root.withdraw()
    dlg = InputDialog(root)
    dlg.grab_set()
    root.wait_window(dlg)
    return dlg.result
