import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QHeaderView, QTableWidgetItem, QPushButton, QLabel, \
    QTableWidget
from PyQt5 import uic
from connection import conn, cur
from par import one_pars
from Pages import *
from Button import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('blade/main_window.ui', self)
        self.setWindowTitle('SaleHunter')
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.profile)
        self.pushButton_3.clicked.connect(self.shops)
        self.pushButton_4.clicked.connect(self.category)
        self.pushButton_5.clicked.connect(self.del_category)
        self.pushButton_5.setVisible(False)
        self.tabs = []
        self.update_tab()
        self.main_load_date()
        self.update_tabs()
        self.initUI()
        self.tabWidget.currentChanged.connect(self.tabChange)

    def initUI(self):

        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(10, 10)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

    def update_tab(self):
        cur.execute("SELECT * FROM Tabs")
        self.tabs = [(QTableWidget(self), i[0], i[1]) for i in cur.fetchall()]

    def add(self):
        now_tab = self.tabWidget.currentIndex()
        if now_tab:
            now_tab = self.tabs[now_tab - 1][1]

        register_page = NewProduct.NewProduct(now_tab)
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
        cur.execute("SELECT * FROM urls order by id")
        products = cur.fetchall()
        self.update_table(self.tableWidget, products)

    def update_table(self, table, products: list):

        title = ["Магазин", "Название", "Характеристика", "Цена, ₽", "GR", "Удалить", 'img']
        table.setColumnCount(len(title))
        table.setHorizontalHeaderLabels(title)
        table.setRowCount(len(products))
        row = 0

        for product in products:
            table.setItem(row, 0, QTableWidgetItem(product[1]))
            table.setItem(row, 1, QTableWidgetItem(product[2]))
            table.setItem(row, 2, QTableWidgetItem(product[8]))
            if not product[4] is None:
                formatted_number = f'{product[4]:,}'.replace(',', ' ')
            else:
                formatted_number = None
            table.setItem(row, 3, QTableWidgetItem(formatted_number))

            btn_gr = QPushButton("")
            btn_gr.setIcon(QIcon('graf4.png'))
            btn_gr.setIconSize(QSize(30, 30))
            btn_gr.setObjectName(str(product[0]))
            btn_gr.clicked.connect(self.price_chart)
            table.setCellWidget(row, 4, btn_gr)

            btn_del = QPushButton("Удалить")
            btn_del.setObjectName(str(product[0]))
            btn_del.clicked.connect(self.confirm_del_product)
            table.setCellWidget(row, 5, btn_del)

            table.setRowHeight(row, 45)

            if product[7]:
                btn_gr = PushButton.PushButton("", other=self, id_name=product[0])
                btn_gr.setIcon(QIcon(f'images/{product[0]}_min.jpg'))
                btn_gr.setIconSize(QSize(40, 40))
                btn_gr.setObjectName(str(product[0]))
                table.setCellWidget(row, 6, btn_gr)

            row += 1

        # table.setColumnWidth(4, 40)
        header = table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)

    def tabChange(self):
        event = self.tabWidget.currentIndex()
        az = self.tabWidget.tabText(event)
        if az != "Главная":
            self.pushButton_5.setVisible(True)
            tab_id = self.tabs[event - 1][1]
            table = self.tabs[event - 1][0]

            cur.execute("SELECT * FROM urls WHERE category = %s", (tab_id,))
            products = cur.fetchall()
            self.update_table(table, products)
        else:
            self.pushButton_5.setVisible(False)
            self.main_load_date()

    def update_tabs(self, flag=False):
        if flag:
            self.tabWidget.addTab(self.tabs[-1][0], self.tabs[-1][2])
        else:
            for tab in self.tabs:
                self.tabWidget.addTab(tab[0], tab[2])

    def confirm_del_product(self):
        az = self.sender().objectName()
        cur.execute(f"SELECT * from urls where id = %s", (int(az),))
        product = cur.fetchone()
        register_page = ConfirmDel.ConfirmDel(product)
        register_page.exec_()
        if register_page.flag:
            self.del_product(product[0])

    def del_product(self, id_product):
        cur.execute(f"DELETE from urls where id = %s", (id_product,))
        self.tabChange()

    def del_category(self):
        event = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(event)
        tab_id = self.tabs[event - 1][1]
        register_page = ConfirmDel.ConfirmDel(name, about=True)
        register_page.exec_()
        if register_page.flag:
            cur.execute(f'Update urls set category = %s where category = %s', (0, tab_id))
            cur.execute(f"DELETE from tabs where id = %s", (tab_id,))
            self.tabWidget.clear()
            self.tabWidget.addTab(self.tableWidget, "Главная")
            self.update_tab()
            self.update_tabs()

    def price_chart(self):
        # az = self.sender().objectName()
        print(555)

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