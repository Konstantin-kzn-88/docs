import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PIL import Image

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Пример'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 100, 100)

        button = QPushButton('PyQt5 button', self)
        button.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        print('Paste')

        im1 = Image.open('img1.jpg')
        im2 = Image.open('img2.jpg')

        im1.paste(im2)
        im1.save('pillow_paste.jpg', quality=95)

        im1.close()
        im2.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())