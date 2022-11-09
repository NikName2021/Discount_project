from PyQt5.QtWidgets import QDialog
import validators

from connection import cur
from PyBlades import add_product


class NewProduct(QDialog, add_product.Ui_Dialog):
    """Окно добавления нового товара"""
    def __init__(self, now_tab):
        self.flag = False
        self.now_tab = now_tab
        super(NewProduct, self).__init__()
        self.setupUi(self)
        cur.execute("SELECT * FROM shops")
        self.comboBox.addItems([i[1] for i in cur.fetchall()])
        # загрузка comboBox и comboBox_2
        self.my_categories = self.category()

        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.close_win)

    def category(self):
        cur.execute("SELECT * FROM Tabs order by id")
        categories = cur.fetchall()
        # загрузка категорий из бд
        categories.append((0, 'Главная'))
        self.comboBox_2.addItems([i[1] for i in categories])
        # добавление категорий в comboBox_2
        undo_category = {i[0]: i[1]for i in categories}
        self.comboBox_2.setCurrentText(undo_category[self.now_tab])
        # устанавливаем выбранную сейчас категорию
        return {i[1]: i[0]for i in categories}

    def close_win(self):
        self.close()

    def run(self):
        name = self.lineEdit.text()
        url = self.lineEdit_2.text()
        shop = self.comboBox.currentText()
        category = self.my_categories[self.comboBox_2.currentText()]
        character = "; ".join(self.textEdit.toPlainText().split('\n'))
        # валидация полей
        if not name:
            self.label_3.setText("Не указано имя")
        elif not url:
            self.label_3.setText("Не указана ссылка")
        elif not validators.url(url):
            self.label_3.setText("Неверная ссылка")
        else:
            # проверка на существование
            cur.execute('SELECT * FROM urls WHERE url = %s', (url,))
            last_product = cur.fetchall()
            if not last_product:
                cur.execute(
                    "INSERT INTO urls (shop, name, url, last_prices, prices, category, character) VALUES (%s, %s, %s, "
                    "%s, %s, %s, %s)",
                    (shop, name, url, 0, 0, category, character))
                if self.checkBox.isChecked():
                    self.flag = True
                self.close()
            else:
                self.label_3.setText("Такой товар уже существует")
