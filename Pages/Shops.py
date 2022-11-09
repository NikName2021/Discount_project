from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QPushButton

from . import ConfirmDel
from . import AddShop
from . import SettingPhoto
from connection import conn, cur
from PyBlades import shops


class Shops(QDialog, shops.Ui_Dialog):
    """Класс диалогового окна для просмотра магазинов и добавления новых"""
    def __init__(self):
        self.flag = False
        super(Shops, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Shops')
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

            # добавление функциональных кнопок в таблицу
            btn_del = QPushButton("")
            btn_del.setIcon(QIcon('config/del1.png'))
            btn_del.setIconSize(QSize(20, 20))
            btn_del.setObjectName(str(shop[0]))
            btn_del.clicked.connect(self.del_product)
            self.tableWidget.setCellWidget(row, 3, btn_del)

            btn_gr = QPushButton("")
            btn_gr.setIcon(QIcon('config/setting.png'))
            btn_gr.setIconSize(QSize(20, 20))
            btn_gr.setObjectName(str(shop[0]))
            btn_gr.clicked.connect(self.setting)
            self.tableWidget.setCellWidget(row, 4, btn_gr)

            row += 1

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def del_product(self):
        id_shop = self.sender().objectName()
        cur.execute("SELECT * FROM shops where id = %s", (int(id_shop),))
        name = cur.fetchone()
        # открытие окна подтверждения удаления
        confirm_del = ConfirmDel.ConfirmDel(name, about=None)
        confirm_del.exec_()
        if confirm_del.flag:
            cur.execute(f"DELETE from shops where id = %s", (int(id_shop),))
            self.load_date(self.load_shop())

    def setting(self):
        id_shop = self.sender().objectName()
        # открытие диалогового окна для добавления тегов для фото
        setting_window = SettingPhoto.SettingPhoto(id_shop)
        setting_window.exec_()

    def run(self):
        # Открытие диалогового окна для добавления нового магазина
        new_shop = AddShop.AddShop()
        new_shop.exec_()
        # если пользователь добавил магазин
        if new_shop.flag:
            self.load_date(self.load_shop())
