from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox


class ProfilePage(QDialog):
    def __init__(self):
        super(ProfilePage, self).__init__()
        uic.loadUi('main_profil.ui', self)
        self.toolButton.clicked.connect(self.help)

    def help(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Help!")
        with open("config/help.txt", 'rt', encoding="UTF-8") as file:
            message = file.read()
        dlg.setText(message)
        button = dlg.exec()