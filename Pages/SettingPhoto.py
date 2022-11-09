from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from connection import conn, cur
from PyBlades import setting_photo


class SettingPhoto(QDialog, setting_photo.Ui_Dialog):
    """Диалоговое окно для добавления параметров фото"""
    def __init__(self, id_shop):
        super(SettingPhoto, self).__init__()
        self.id_shop = int(id_shop)
        self.setupUi(self)
        self.setWindowTitle('Setting_Photo')
        self.start_page()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.close_win)

    def start_page(self):
        # подгрузка существующих данных
        cur.execute('SELECT * FROM shops WHERE id = %s', (self.id_shop,))
        setting = cur.fetchone()
        self.lineEdit.setText(setting[4])
        self.lineEdit_2.setText(setting[5])

    def run(self):
        type_class = self.lineEdit.text()
        name_class = self.lineEdit_2.text()
        # валидация полей
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