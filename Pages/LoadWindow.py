from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QDialog
from par import one_pars


class Downloader(QThread):
    """ Класс потока для запуска парсинга"""
    def __init__(self, product):
        super().__init__()
        self.product = product

    def run(self):
        one_pars(self.product)


class LoadWindow(QDialog):
    """Окно ожидания загрузки"""

    def __init__(self, product):
        super(LoadWindow, self).__init__()
        uic.loadUi('blade/load.ui', self)
        self.setWindowTitle('Loading')
        self.product = product

        self.run(self.product)

    def run(self, product):
        # открытие потока для парсинга
        self.downloader = Downloader(product)

        # Qt вызовет метод `downloadFinished()`, когда поток завершится.

        self.downloader.finished.connect(self.downloadFinished)
        self.downloader.start()

    def downloadFinished(self):
        del self.downloader
        self.close()