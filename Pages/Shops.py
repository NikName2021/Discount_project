from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QPushButton

from connection import conn, cur


class Shops(QDialog):
    def __init__(self):
        self.flag = False
        super(Shops, self).__init__()
        uic.loadUi('blade/shops.ui', self)
        self.load_date(self.load_shop())
        self.pushButton.clicked.connect(self.run)

    def load_shop(self):
        cur.execute("SELECT * FROM shops")
        return cur.fetchall()

    def load_date(self, shops):

        title = ["Магазин", "Название класса", "Тип", "Del", "Sett"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(shops))
        row = 0

        for shop in shops:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(shop[1]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(shop[2]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(shop[3]))

            btn_del = QPushButton("")
            btn_del.setIcon(QIcon('del1.png'))
            btn_del.setIconSize(QSize(30, 30))
            btn_del.setObjectName(str(shop[0]))
            btn_del.clicked.connect(self.setting)
            self.tableWidget.setCellWidget(row, 3, btn_del)

            btn_gr = QPushButton("")
            btn_gr.setIcon(QIcon('setting.png'))
            btn_gr.setIconSize(QSize(30, 30))
            btn_gr.setObjectName(str(shop[0]))
            btn_gr.clicked.connect(self.setting)
            self.tableWidget.setCellWidget(row, 4, btn_gr)

            row += 1

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def del_product(self):
        id_shop = self.sender().objectName()
        cur.execute(f"DELETE from shops where id = %s", (int(id_shop),))
        self.load_date(self.load_shop())

    def setting(self):
        id_shop = self.sender().objectName()
        register_page = SettingPhoto(id_shop)
        register_page.exec_()

    def run(self):
        register_page = AddShop()
        register_page.exec_()
        if register_page.flag:
            self.load_date(self.load_shop())


class AddShop(QDialog):
    def __init__(self):
        super(AddShop, self).__init__()
        uic.loadUi('blade/add_shop.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.close_win)
        self.flag = False

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

    def close_win(self):
        self.close()


class SettingPhoto(QDialog):
    def __init__(self, id_shop):
        super(SettingPhoto, self).__init__()
        self.id_shop = int(id_shop)
        uic.loadUi('blade/setting_photo.ui', self)
        self.start_page()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.close_win)

    def start_page(self):
        cur.execute('SELECT * FROM shops WHERE id = %s', (self.id_shop,))
        setting = cur.fetchone()
        self.lineEdit.setText(setting[4])
        self.lineEdit_2.setText(setting[5])

    def run(self):
        type_class = self.lineEdit.text()
        name_class = self.lineEdit_2.text()
        if not type_class:
            self.label_4.setText("Не указан класс")
        elif not name_class:
            self.label_4.setText("Не указано название класса")

        else:
            cur.execute("UPDATE shops set image_key = %s, image_type_key = %s where id = %s",
                        (type_class, name_class, self.id_shop))
            self.close()

    def close_win(self):
        self.close()