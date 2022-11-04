import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QDialog, QHeaderView, QTableWidgetItem, QPushButton, QMessageBox, QTabWidget, QWidget, QLabel, \
    QTableWidget
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
        self.tabs = []
        self.update_tab()
        self.main_load_date()
        self.update_tabs()
        self.tabWidget.currentChanged.connect(self.tabChange)

    def update_tab(self):
        cur.execute("SELECT * FROM Tabs")
        self.tabs = [(QTableWidget(self), i[0], i[1]) for i in cur.fetchall()]

    def add(self):
        now_tab = self.tabWidget.currentIndex()
        if now_tab:
            now_tab = self.tabs[now_tab - 1][1]

        register_page = RegisterPage.RegisterPage(now_tab)
        register_page.exec_()
        if register_page.flag:
            self.tabChange()
            cur.execute('SELECT * FROM urls ORDER BY id DESC LIMIT 1')
            one_pars(cur.fetchone())
            self.main_load_date()

    def profile(self):
        register_page = Profile.ProfilePage()
        register_page.exec_()

    def category(self):
        register_page = AddCategory.AddCategory()
        register_page.exec_()
        if register_page.flag:
            self.update_tab()
            self.update_tabs(True)

    def shops(self):
        register_shop = Shops.Shops()
        register_shop.exec_()

    def main_load_date(self):
        cur.execute("SELECT * FROM urls")
        products = cur.fetchall()
        self.update_table(self.tableWidget, products)

    def update_table(self, table, products: list):

        title = ["Магазин", "Название", "Ссылка", "Цена, ₽", "GR", "Удалить"]
        table.setColumnCount(len(title))
        table.setHorizontalHeaderLabels(title)
        table.setRowCount(len(products))
        row = 0

        for person in products:
            table.setItem(row, 0, QTableWidgetItem(person[1]))
            table.setItem(row, 1, QTableWidgetItem(person[2]))
            table.setItem(row, 2, QTableWidgetItem(person[3]))
            if not person[4] is None:
                formatted_number = f'{person[4]:,}'.replace(',', ' ')
            else:
                formatted_number = None
            table.setItem(row, 3, QTableWidgetItem(formatted_number))

            btn_gr = QPushButton("")
            btn_gr.setIcon(QIcon('graf3.png'))
            btn_gr.setIconSize(QSize(40, 40))
            btn_gr.setObjectName(str(person[0]))
            btn_gr.clicked.connect(self.price_chart)
            table.setCellWidget(row, 4, btn_gr)

            btn_del = QPushButton("Удалить")
            btn_del.setObjectName(str(person[0]))
            btn_del.clicked.connect(self.del_product)
            table.setCellWidget(row, 5, btn_del)

            row += 1

        header = table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)

    def tabChange(self):
        event = self.tabWidget.currentIndex()
        az = self.tabWidget.tabText(event)
        if az != "Главная":
            tab_id = self.tabs[event - 1][1]
            table = self.tabs[event - 1][0]

            cur.execute("SELECT * FROM urls WHERE category = %s", (tab_id,))
            products = cur.fetchall()
            self.update_table(table, products)
        else:
            self.main_load_date()

    def update_tabs(self, flag=False):
        if flag:
            self.tabWidget.addTab(self.tabs[-1][0], self.tabs[-1][2])
        else:
            for tab in self.tabs:
                self.tabWidget.addTab(tab[0], tab[2])

    def del_product(self):
        az = self.sender().objectName()
        cur.execute(f"DELETE from urls where id = %s", (int(az),))
        self.tabChange()

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