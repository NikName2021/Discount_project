from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QPushButton
import validators
from connection import conn, cur


class Add_shop(QDialog):
    def __init__(self):
        super(Add_shop, self).__init__()
        uic.loadUi('add_shop.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.close_win)
        self.flag = False

    def close_win(self):
        self.close()

    def run(self):
        name_shop = self.lineEdit.text()
        type_class = self.lineEdit_2.text()
        name_class = self.lineEdit_3.text()
        if not name_shop:
            self.label_4.setText("Не указано имя")
        elif not type_class:
            self.label_4.setText("Не указан тип")
        elif not name_class:
            self.label_4.setText("Не указано название класса")

        else:
            cur.execute('SELECT * FROM shops WHERE name = %s', (name_shop,))
            last_product = cur.fetchall()
            if not last_product:
                cur.execute("INSERT INTO shops (name, key, type_key) VALUES (%s, %s, %s)",
                            (name_shop, name_class, type_class))
                self.flag = True
                self.close()
            else:
                self.label_4.setText("Такой магазин уже существует")


class Shops(QDialog):
    def __init__(self):
        self.flag = False
        super(Shops, self).__init__()
        uic.loadUi('shops.ui', self)
        self.load_date(self.load_shop())
        self.pushButton.clicked.connect(self.run)

    def load_shop(self):
        cur.execute("SELECT * FROM shops")
        return cur.fetchall()

    def load_date(self, shops):

        title = ["Магазин", "Название класса", "Тип", "Удалить"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(shops))
        row = 0

        for shop in shops:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(shop[1]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(shop[2]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(shop[3]))

            btn_del = QPushButton("Удалить")
            btn_del.setObjectName(str(shop[0]))
            btn_del.clicked.connect(self.del_product)
            self.tableWidget.setCellWidget(row, 3, btn_del)

            row += 1

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def del_product(self):
        pass

    def run(self):
        register_page = Add_shop()
        register_page.exec_()
        if register_page.flag:
            self.load_date(self.load_shop())