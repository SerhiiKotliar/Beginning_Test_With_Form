import sys
from PySide6.QtWidgets import QApplication, QDialog
from form import Ui_Dialog
from PySide6.QtCore import Qt

# клас що працює з формою налаштування тестів
class MyDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)   # створює інтерфейс
        # окно поверх всех
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        # модальный режим (блокирует остальные окна приложения)
        self.setModal(True)
        # тут можна прив'язати кнопки, наприклад:
        self.btnOk.clicked.connect(self.on_ok)
        self.btnCnl.clicked.connect(self.close)


    def on_ok(self):
        """Читаємо дані з форми"""
        # Комбобокс (розкладка)
        localiz = self.cmbLocaliz.currentText()

        # Радіокнопки (регістр)
        register = self.cmbLocaliz_2.currentText()

        # Чекбокси
        cyfry = self.chkbCyfry.isChecked()
        spec = self.chkbSpecS.isChecked()
        probel = self.chkbProbel.isChecked()
        email_in = self.chkbEmail.isChecked()
        url_in = self.chkbURL.isChecked()

        # Спінбокси
        len_min = self.spinBoxLenMin.value()
        len_max = self.spinBoxLenMax.value()

        # Вивід результатів у консоль
        # print("🔹 Дані з форми:")
        # print(f"Розкладка: {localiz}")
        # print(f"Регістр: {register}")
        # print(f"Цифри: {cyfry}")
        # print(f"Спецсимволи: {spec}")
        # print(f"Пробіли: {probel}")
        # print(f"Мін. довжина: {len_min}")
        # print(f"Макс. довжина: {len_max}")
        self.result = {"register": register, "localiz": localiz, "cyfry": cyfry, "spec": spec, "probel": probel, "len_min": len_min, "len_max": len_max, "email_in": email_in, "url_in": url_in}
        # Закриваємо діалог
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = MyDialog()
    dlg.show()
    sys.exit(app.exec())
