import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QHeaderView, QTableWidgetItem, QPushButton, QLabel, QTableWidget

from connection import conn, cur
from Pages import *
from Button import *
from PyBlades import main_window


class MyWidget(QMainWindow, main_window.Ui_MainWindow):
    """Главное окно приложения Sale-Hunter"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('SaleHunter')
        self.TABLE_STYLE = """
                     background-color: rgb(251, 253, 255);
                     font: 10pt "Segoe UI";
                 """

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
        # Инициализация места для фотографии

        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(10, 10)
        self.image.setPixmap(self.pixmap)

    def update_tab(self, flag=False):
        # загрузка категорий
        cur.execute("SELECT * FROM Tabs")
        if flag:
            tab = cur.fetchall()[-1]
            self.tabs.append((QTableWidget(self), tab[0], tab[1]))
        else:
            self.tabs = [(QTableWidget(self), i[0], i[1]) for i in cur.fetchall()]

    def add(self):
        # добавление нового товара
        # получение id категории
        now_tab = self.tabWidget.currentIndex()
        if now_tab:
            now_tab = self.tabs[now_tab - 1][1]

        # окно добавления продукта
        add_new_product = NewProduct.NewProduct(now_tab)
        add_new_product.exec_()
        self.tabChange()
        if add_new_product.flag:
            # загрузка данных по товару
            cur.execute('SELECT * FROM urls ORDER BY id DESC LIMIT 1')
            load_page = LoadWindow.LoadWindow(cur.fetchone())
            load_page.exec_()
            self.tabChange()

    def profile(self):
        # открытие окна с профилем
        profile = Profile.ProfilePage()
        profile.exec_()

    def category(self):
        # окно добавления категории
        new_category = AddCategory.AddCategory()
        new_category.exec_()
        if new_category.flag:
            # обновление списка с категориями и таблицами
            self.update_tab(True)
            self.update_tabs(True)

    def shops(self):
        all_shops = Shops.Shops()
        all_shops.exec_()
        if all_shops.flag_on_del:
            self.tabChange()

    def main_load_date(self):
        # получение товаров для главной категории(все товары из бд)
        cur.execute("SELECT * FROM urls order by id")
        products = cur.fetchall()
        self.update_table(self.tableWidget, products)

    def update_table(self, table, products):
        # загрузка товаров в таблицу
        title = ["Магазин", "Название", "Характеристика", "Цена, ₽", "GR", "Удалить", 'Img']
        table.setStyleSheet(self.TABLE_STYLE)
        table.setColumnCount(len(title))
        table.setHorizontalHeaderLabels(title)
        table.setRowCount(len(products))
        row = 0

        for product in products:

            table.setItem(row, 0, QTableWidgetItem(product[1]))
            url = QLabel(f'<a style="color: rgb(0, 0, 0); text-decoration: none;" href={product[3]}>{product[2]}</a>',
                         openExternalLinks=True)
            table.setCellWidget(row, 1, url)

            table.setItem(row, 2, QTableWidgetItem(product[8]))
            if not product[4] is None:
                formatted_number = f'{product[4]:,}'.replace(',', ' ')
            else:
                formatted_number = None
            table.setItem(row, 3, QTableWidgetItem(formatted_number))

            btn_gr = QPushButton("")
            btn_gr.setIcon(QIcon('config/graf4.png'))
            btn_gr.setIconSize(QSize(33, 33))
            btn_gr.setObjectName(str(product[0]))
            btn_gr.clicked.connect(self.price_chart)
            table.setCellWidget(row, 4, btn_gr)

            btn_del = QPushButton("")
            btn_del.setIcon(QIcon('config/trash.jpg'))
            btn_del.setIconSize(QSize(28, 28))
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
        # при переходе в другую категорию:
        event = self.tabWidget.currentIndex()
        az = self.tabWidget.tabText(event)
        if az != "Главная":
            self.pushButton_5.setVisible(True)
            # появление кнопки для удаления категории
            try:
                tab_id = self.tabs[event - 1][1]
                table = self.tabs[event - 1][0]
                cur.execute("SELECT * FROM urls WHERE category = %s order by id", (tab_id,))
                products = cur.fetchall()
                # загрузка данных в нужную таблицу
                self.update_table(table, products)
            except IndexError:
                pass

        else:
            self.pushButton_5.setVisible(False)
            self.main_load_date()

    def update_tabs(self, flag=False):
        if flag:
            # добавление одного tab
            self.tabWidget.addTab(self.tabs[-1][0], self.tabs[-1][2])
        else:
            # добавление всех
            for tab in self.tabs:
                self.tabWidget.addTab(tab[0], tab[2])

    def confirm_del_product(self):
        az = self.sender().objectName()
        cur.execute(f"SELECT * from urls where id = %s", (int(az),))
        product = cur.fetchone()
        # окно подтверждения удаления продукта
        conf_del = ConfirmDel.ConfirmDel(product)
        conf_del.exec_()
        if conf_del.flag:
            self.del_product(product[0])

    def del_product(self, id_product):
        # удаление продукта
        cur.execute(f"DELETE from urls where id = %s", (id_product,))
        self.tabChange()

    def del_category(self):
        event = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(event)
        tab_id = self.tabs[event - 1][1]
        # окно подтверждения удаления категории
        confirm_del = ConfirmDel.ConfirmDel(name, about=True)
        confirm_del.exec_()
        if confirm_del.flag:
            cur.execute(f'Update urls set category = %s where category = %s', (0, tab_id))
            # переход всех товаров на главную
            cur.execute(f"DELETE from tabs where id = %s", (tab_id,))
            # удаление категории
            self.tabWidget.clear()
            # очистка всех категорий из окна и новая инициализация их
            self.tabWidget.addTab(self.tableWidget, "Главная")
            self.update_tab()
            self.update_tabs()

    def price_chart(self):
        # построение графика цены для товара
        az = self.sender().objectName()
        graf_page = GrafOfPrice.GrafOfPrice(az)
        graf_page.exec_()

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

