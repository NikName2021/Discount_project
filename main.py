import sys
import validators
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QDialog, QHeaderView, QTableWidgetItem, QPushButton, QMessageBox
from PyQt5 import uic
from connection import con, cur
from par import one_pars


class RegisterPage(QDialog):
    def __init__(self):
        super(RegisterPage, self).__init__()
        uic.loadUi('add_product.ui', self)
        names = [i[1] for i in cur.execute("SELECT * FROM shops").fetchall()]
        self.comboBox.addItems(names)
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
            last_product = cur.execute('SELECT * FROM urls WHERE url = ?', (url,)).fetchone()
            if not last_product:
                cur.execute("INSERT INTO urls (shop, name, url, last_price, prices) VALUES (?, ?, ?, ?, ?)",
                            (shop, name, url, 0, 0))
                con.commit()
                self.close()
            else:
                self.label_3.setText("Такой товар уже существует")


class ProfilePage(QDialog):
    def __init__(self):
        super(ProfilePage, self).__init__()
        uic.loadUi('main_profil.ui', self)
        self.toolButton.clicked.connect(self.help)

    def help(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Help!")
        with open("help.txt", 'rt', encoding="UTF-8") as file:
            message = file.read()
        dlg.setText(message)
        button = dlg.exec()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.profile)
        self.load_date()

    def add(self):
        register_page = RegisterPage()
        register_page.exec_()
        self.load_date()
        # last_product = cur.execute('SELECT * FROM urls ORDER BY id DESC LIMIT 1').fetchone()
        # one_pars(last_product)
        # self.load_date()

    def profile(self):
        register_page = ProfilePage()
        register_page.exec_()

    def load_date(self):
        products = cur.execute("SELECT * FROM urls").fetchall()

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
        # self.tableWidget.itemChanged.connect(self.main)

    def del_product(self):
        az = self.sender().objectName()
        cur.execute(f"DELETE from urls where id = ?", (int(az),))
        con.commit()
        self.load_date()

    def price_chart(self):
        az = self.sender().objectName()
        print(az)

    def closeEvent(self, event):
        con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())