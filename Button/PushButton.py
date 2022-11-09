from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton
from PIL import Image


class PushButton(QPushButton):
    def __init__(self, parent=None, other=1, id_name=1):
        super(PushButton, self).__init__(parent)
        self.window = other
        self.id_name = id_name

    def enterEvent(self, event):
        try:
            img = Image.open(f'./images/{self.id_name}_avg.jpg')
            # получаем ширину и высоту
            width, height = img.size
            x = event.windowPos().x()
            y = event.windowPos().y()
            height_img = int(y - height)
            if height_img < 0:
                height_img = 30

            main = QPixmap(f'./images/{self.id_name}_avg.jpg')
            self.window.image.move(int(x - width) - 15, height_img)
            self.window.image.resize(width, height)
            self.window.image.setPixmap(main)

        except Exception as ex:
            print(ex)

    def leaveEvent(self, event):
        main = QPixmap("")
        self.window.image.move(10, 10)
        self.window.image.resize(10, 10)
        self.window.image.setPixmap(main)
