from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox


class ProfilePage(QDialog):
    """Окно профиля с кнопкой help"""

    def __init__(self):
        super(ProfilePage, self).__init__()
        uic.loadUi('blade/main_profil.ui', self)
        self.setWindowTitle('Profile')
        self.toolButton.clicked.connect(self.help)

    def help(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Help!")
        with open("config/help.txt", 'rt', encoding="UTF-8") as file:
            message = file.read()
        dlg.setText(message)
        button = dlg.exec()