from PyQt5.QtWidgets import QDialog, QMessageBox

from PyBlades import main_profil


class ProfilePage(QDialog, main_profil.Ui_Dialog):
    """Окно профиля с кнопкой help"""

    def __init__(self):
        super(ProfilePage, self).__init__()
        self.setWindowTitle('Profile')
        self.setupUi(self)
        self.toolButton.clicked.connect(self.help)
        self.pushButton.clicked.connect(self.add_telegram)
        self.UI()

    def UI(self):
        with open('config/profile.txt', 'rt', encoding='UTF-8') as file:
            id_user = file.readline()
        self.lineEdit.setText(id_user)

    def add_telegram(self):
        name = self.lineEdit.text()
        try:
            if name != "":
                name = int(name)
        except ValueError:
            self.label_4.setText('Неверный id')
            return
        with open('config/profile.txt', 'wt', encoding='UTF-8') as file:
            file.write(str(name))
        self.label_4.setText('Сохранено')

    def help(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Help!")
        with open("config/help.txt", 'rt', encoding="UTF-8") as file:
            message = file.read()
        dlg.setText(message)
        button = dlg.exec()