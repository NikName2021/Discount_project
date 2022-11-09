from PyQt5.QtWidgets import QDialog
from connection import conn, cur

from PyBlades import add_category


class AddCategory(QDialog, add_category.UiAddCategory):
    """ Окно добавления новой категории"""
    def __init__(self):
        self.flag = False
        super(AddCategory, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('NewCategory')
        self.check_len()
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.close_win)

    def check_len(self):
        cur.execute("SELECT * FROM tabs")
        names = cur.fetchall()
        if len(names) == 10:
            self.label_2.setText("Нельзя создавать больше 10 категорий")
            self.pushButton_2.setVisible(False)

    def run(self):
        name = self.lineEdit.text()
        # валидация
        if not name:
            self.label_2.setText("Не указано имя")
        else:
            cur.execute("SELECT * FROM tabs")
            names = [i[1] for i in cur.fetchall()]
            # проверка на существование
            if name not in names:
                cur.execute("INSERT INTO tabs (name) VALUES (%s)", (name,))
                self.flag = True
                self.close()
            else:
                self.label_2.setText("Такая категория существует")

    def close_win(self):
        self.close()