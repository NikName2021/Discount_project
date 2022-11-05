from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox


class ConfirmDel(QDialog):
    def __init__(self, product, about=False):
        super(ConfirmDel, self).__init__()
        self.flag = False
        self.about = about
        self.product = product
        uic.loadUi('blade/confirm_del.ui', self)
        self.initUI()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.cancel)

    def initUI(self):

        self.label_2.setWordWrap(True)
        if self.about:
            self.label_2.setText(f"""Вы уверены, что хотите удалить категорию: {self.product} ?

Все товары из нее окажутся в главной категории""")

        else:
            self.label_2.setText(f"""Вы уверены, что хотите удалить товар: {self.product[2]}({self.product[1]})

            Все его данные будут удалены без возможности восстановления!""")

    def run(self):
        self.flag = True
        self.close()

    def cancel(self):
        self.close()
