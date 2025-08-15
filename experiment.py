import tkinter as tk
from tkinter import messagebox

class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Введення тестових даних")
        # self.geometry("500x400")
        self.attributes('-topmost', True)
        # self.center_window(500, 400)

        self.required_vars = {}
        self.labels = {}  # для хранения текста лейблов

        fields = (
            ("Логін:", "login", ""),
            ("Пароль:", "password", ""),
            ("Адреса (URL):", "url", "")
            # ("Кількість навчальних зразків:", "count_train", "554"),
            # ("Кількість контрольних навчальних зразків:", "count_contr", "54"),
            # ("Розмір пакету зразків:", "batch", "555"),
            # ("Кількість епох навчання:", "epoch", "87"),
        )

        for row, (label_text, attr_name, default) in enumerate(fields):
            lbl = tk.Label(self, text=label_text)
            lbl.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            self.labels[attr_name] = label_text  # сохраняем текст лейбла

            entry = tk.Entry(self)
            entry.insert(0, default)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
            setattr(self, attr_name, entry)

            var = tk.BooleanVar()
            chk = tk.Checkbutton(self, text="Обов'язкове", variable=var)
            chk.grid(row=row, column=2, padx=5, pady=5, sticky="w")
            self.required_vars[attr_name] = var

        # Кнопка OK
        self.submit_button = tk.Button(self, text="OK", command=self.on_button_click)
        self.submit_button.grid(row=len(fields), column=0, pady=10, sticky="we", padx=5)

        # Кнопка Cancel
        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=len(fields), column=1, pady=10, sticky="we", padx=5)

        self.bind("<Return>", self.on_button_click)

        self.result = None
        self.columnconfigure(1, weight=1)



    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_button_click(self, event=None):
        # Проверка обязательных полей
        missing_fields = []
        for name, var in self.required_vars.items():
            if var.get():  # если поле обязательное
                value = getattr(self, name).get().strip()
                if not value:
                    missing_fields.append(self.labels[name])  # используем текст лейбла

        if missing_fields:
            messagebox.showerror(
                "Помилка",
                "Будь ласка, заповніть обов'язкові поля:\n" + "\n".join(missing_fields),
                parent=self  # <-- окно ошибки поверх диалога
            )
            return  # не закрываем диалог

        # Все обязательные поля заполнены — сохраняем результат и закрываем
        self.result = {
            "login": self.login.get(),
            "password": self.password.get(),
            "url": self.url.get(),
            # "count_train": self.count_train.get(),
            # "count_contr": self.count_contr.get(),
            # "batch": self.batch.get(),
            # "epoch": self.epoch.get(),
            # "required": {k: v.get() for k, v in self.required_vars.items()}
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()


# Тест
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    dialog = InputDialog(root)
    root.wait_window(dialog)
    print(dialog.result)
