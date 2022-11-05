from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from par import one_pars


class LoadWindow(QDialog):
    """Окно ожидания загрузки"""

    def __init__(self, product):
        super(LoadWindow, self).__init__()
        uic.loadUi('blade/load.ui', self)
        self.product = product

        self.run(self.product)

    def run(self, product):
        one_pars(product)
        self.close()

