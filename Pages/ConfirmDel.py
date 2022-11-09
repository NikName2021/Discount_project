from PyQt5.QtWidgets import QDialog

from PyBlades import confirm_del


class ConfirmDel(QDialog, confirm_del.UIConfirmDel):
    """Окно для подтверждения всех удалений"""
    def __init__(self, product, about=False):
        super(ConfirmDel, self).__init__()
        self.flag = False
        self.about = about
        self.product = product
        self.setupUi(self)
        self.initUI()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.cancel)

    def initUI(self):
        # разное наполнение label для разных подтверждений
        self.label_2.setWordWrap(True)
        if self.about is None:
            self.label_2.setText(f"""Вы уверены, что хотите удалить магазин: {self.product[1]} ?

Все товары из этого магазина будут удалены!""")

        elif self.about:
            self.label_2.setText(f"""Вы уверены, что хотите удалить категорию: {self.product} ?

Все товары из нее окажутся только в главной категории""")

        else:
            self.label_2.setText(f"""Вы уверены, что хотите удалить товар: {self.product[2]}({self.product[1]})

Все его данные будут удалены без возможности восстановления!""")

    def run(self):
        # пользователь подтвердил удаление
        self.flag = True
        self.close()

    def cancel(self):
        self.close()