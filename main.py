import sys
import validators
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QDialog, QHeaderView, QTableWidgetItem, QPushButton
from PyQt5 import uic
from connection import con, cur


class RegisterPage(QDialog):
    def __init__(self):
        super(RegisterPage, self).__init__()
        uic.loadUi('add_product.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.close_win)

    def close_win(self):
        self.close()

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
            cur.execute("INSERT INTO urls (shop, name, url) VALUES (?, ?, ?)", (shop, name, url))
            con.commit()
            self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.load_date()

    def run(self):
        register_page = RegisterPage()
        register_page.exec_()
        self.load_date()

    def load_date(self):
        products = cur.execute("SELECT * FROM urls").fetchall()

        title = ["Магазин", "Название", "Ссылка", "GR", "Удалить"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(products))
        row = 0

        for person in products:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(person[1]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(person[2]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(person[3]))

            btn = QPushButton("GR")
            btn.setObjectName(str(person[0]))
            btn.clicked.connect(self.price_chart)
            self.tableWidget.setCellWidget(row, 3, btn)

            btn = QPushButton("Удалить")
            btn.setObjectName(str(person[0]))
            btn.clicked.connect(self.del_product)
            self.tableWidget.setCellWidget(row, 4, btn)

            row += 1

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        # self.tableWidget.itemChanged.connect(self.main)

    def del_product(self):
        az = self.sender().objectName()
        cur.execute(f"DELETE from urls where id = ?", (int(az),))
        con.commit()
        self.load_date()

    def price_chart(self):
        az = self.sender().objectName()
        print(az)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.excepthook = except_hook
sys.exit(app.exec_())