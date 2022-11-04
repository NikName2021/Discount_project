from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import validators
from connection import cur


class RegisterPage(QDialog):
    def __init__(self, now_tab):
        self.flag = False
        self.now_tab = now_tab
        super(RegisterPage, self).__init__()
        uic.loadUi('blade/add_product.ui', self)
        cur.execute("SELECT * FROM shops")
        names = [i[1] for i in cur.fetchall()]
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
            cur.execute('SELECT * FROM urls WHERE url = %s', (url,))
            last_product = cur.fetchall()
            if not last_product:
                cur.execute(
                    "INSERT INTO urls (shop, name, url, last_prices, prices, category) VALUES (%s, %s, %s, %s, %s, %s)",
                    (shop, name, url, 0, 0, self.now_tab))
                self.flag = True
                self.close()
            else:
                self.label_3.setText("Такой товар уже существует")