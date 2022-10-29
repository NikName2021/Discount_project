import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QDialog, QHeaderView, QTableWidgetItem, QPushButton, QMessageBox, QTabWidget, QWidget, QLabel
from PyQt5 import uic
from connection import conn, cur
from par import one_pars
from clasiss import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.profile)
        self.pushButton_3.clicked.connect(self.shops)
        self.pushButton_4.clicked.connect(self.category)
        self.load_date()

    def add(self):
        register_page = RegisterPage.RegisterPage()
        register_page.exec_()
        if register_page.flag:
            self.load_date()
            cur.execute('SELECT * FROM urls ORDER BY id DESC LIMIT 1')
            one_pars(cur.fetchone())
            self.load_date()

    def profile(self):
        register_page = Profile.ProfilePage()
        register_page.exec_()

    def category(self):
        register_page = AddCategory.AddCategory()
        register_page.exec_()
        if register_page.flag:
            self.update_tabs(True)

    def shops(self):
        register_shop = Shops.Shops()
        register_shop.exec_()

    def load_date(self):
        cur.execute("SELECT * FROM urls")
        products = cur.fetchall()

        title = ["Магазин", "Название", "Ссылка", "Цена, ₽", "GR", "Удалить"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(products))
        row = 0

        for person in products:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(person[1]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(person[2]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(person[3]))
            if not person[4] is None:
                formatted_number = f'{person[4]:,}'.replace(',', ' ')
            else:
                formatted_number = None
            self.tableWidget.setItem(row, 3, QTableWidgetItem(formatted_number))

            btn_gr = QPushButton("")
            btn_gr.setIcon(QIcon('graf3.png'))
            btn_gr.setIconSize(QSize(40, 40))
            btn_gr.setObjectName(str(person[0]))
            btn_gr.clicked.connect(self.price_chart)
            self.tableWidget.setCellWidget(row, 4, btn_gr)

            btn_del = QPushButton("Удалить")
            btn_del.setObjectName(str(person[0]))
            btn_del.clicked.connect(self.del_product)
            self.tableWidget.setCellWidget(row, 5, btn_del)

            row += 1

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabWidget.currentChanged.connect(self.TabChange)
        self.tabWidget.setMovable(True)
        self.update_tabs()

        # self.tableWidget.itemChanged.connect(self.main)

    def update_tabs(self, flag=False):
        if flag:
            cur.execute("SELECT * FROM Tabs ORDER BY id DESC LIMIT 1")
        else:
            cur.execute("SELECT * FROM Tabs")
        tabs = cur.fetchall()
        for tab in tabs:
            tab1 = QWidget()
            tab1.setObjectName(str(tab[0]))
            self.tabWidget.addTab(tab1, tab[1])

    def TabChange(self, event):
        az = self.tabWidget.tabText(event)
        print(event)
        print(az)

    def del_product(self):
        az = self.sender().objectName()
        cur.execute(f"DELETE from urls where id = %s", (int(az),))
        self.load_date()

    def price_chart(self):
        az = self.sender().objectName()
        print(az)

    def closeEvent(self, event):
        conn.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())