from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
import validators
from connection import conn, cur


class Shops(QDialog):
    def __init__(self):
        self.flag = False
        super(Shops, self).__init__()
        uic.loadUi('shops.ui', self)
        cur.execute("SELECT * FROM shops")
        shops = cur.fetchall()
        self.pushButton.clicked.connect(self.run)
        self.load_date(shops)

    def load_date(self, shops):

        title = ["Магазин", "Название класса", "Тип"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(shops))
        row = 0

        for shop in shops:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(shop[1]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(shop[2]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(shop[3]))


            # btn_del = QPushButton("Удалить")
            # btn_del.setObjectName(str(person[0]))
            # btn_del.clicked.connect(self.del_product)
            # self.tableWidget.setCellWidget(row, 5, btn_del)

            row += 1

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # self.tableWidget.itemChanged.connect(self.main)


    def run(self):
        name = self.lineEdit.text()
        url = self.lineEdit_2.text()
        shop = self.comboBox.currentText()
        if not name:
            self.label_3.setText("Не указано имя")
        elif not url:
            self.label_3.setText("Не указана ссылка")
        elif not validators.url(url):
            self.label_3.setText("Неверная ссылка")
        else:
            cur.execute('SELECT * FROM urls WHERE url = %s', (url,))
            last_product = cur.fetchall()
            if not last_product:
                cur.execute("INSERT INTO urls (shop, name, url, last_prices, prices) VALUES (%s, %s, %s, %s, %s)",
                            (shop, name, url, 0, 0))
                self.flag = True
                self.close()
            else:
                self.label_3.setText("Такой товар уже существует")