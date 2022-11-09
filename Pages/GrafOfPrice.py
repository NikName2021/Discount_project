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
        self.setWindowTitle('Graph')
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

        discount = [i[2] for i in prices]  # все ценники для товара
        count = [i for i in range(len(prices))]  # количество ценников по x
        signature = [i[3]+timedelta(hours=3) for i in prices]  # добавление 3 часов к всемирному времени

        # все время для ценников
        signature = [str(i.strftime("%d.%m.%y _ %H.%M")) for i in signature]
        axes = self.figure.subplots()

        # axes.hlines(y=discount, xmin=0, xmax=len(count),  color='gray',  linewidth=1, linestyles='dashdot')
        # axes.scatter(y=discount, x=count, color='firebrick',)

        axes.vlines(count, ymin=0, ymax=discount, color="y")
        axes.plot(count, discount, "o", color="y")

        axes.set_ylim(0, int(max(discount) * 1.3))
        axes.set_xticks(count)
        axes.set_xticklabels(signature, rotation=30,
                           fontdict={'horizontalalignment': 'right', 'size': 8})

        for i_x, i_y in zip(count, discount):
            axes.text(i_x, i_y, i_y, horizontalalignment='center', verticalalignment='bottom')

        self.canvas.draw()

