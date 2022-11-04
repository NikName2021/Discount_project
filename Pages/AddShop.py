from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QPushButton
from connection import conn, cur


class Add_shop(QDialog):
    def __init__(self):
        super(Add_shop, self).__init__()
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