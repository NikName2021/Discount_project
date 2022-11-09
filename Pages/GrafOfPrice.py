from PyQt5.QtWidgets import QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from datetime import timedelta
from connection import cur
from PyBlades import graf_matrolib


class GrafOfPrice(QDialog, graf_matrolib.Ui_Dialog):
    """Окно построения графика по цене"""
    def __init__(self, id_product):
        super(GrafOfPrice, self).__init__()
        self.setupUi(self)
        self.id_product = int(id_product)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.plot()

    def plot(self):
        cur.execute(f"SELECT * from prices where id_product = %s order by id", (self.id_product,))
        prices = cur.fetchall()

        discount = [0] + [i[2] for i in prices]  # все ценники для товара
        count = [i for i in range(len(prices) + 1)]  # количество ценников по x
        signature = [i[3]+timedelta(hours=3) for i in prices]  # добавление 3 часов к всемирному времени

        # все время для ценников
        signature = [0] + [i.strftime("%y.%m.%d:%H.%M.%S") for i in signature]

        ax = self.figure.add_subplot(111)
        # построение графика
        ax.plot(count, discount, '-')
        # замена нумераций на время
        ax.set_xticks(count, labels=signature)

        self.canvas.draw()

