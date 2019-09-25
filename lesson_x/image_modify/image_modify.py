import sys
from PyQt5.QtWidgets import (QMainWindow, QLabel, QAction, QFileDialog, QApplication, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.fname = None

    def initUI(self):

        self.lbl = QLabel(self)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Открыть файл')
        openFile.triggered.connect(self.showDialog)

        set_bw = QAction('BW', self)
        set_bw.triggered.connect(self.bw)

        set_gray = QAction('gray', self)
        set_gray.triggered.connect(self.gray)

        set_negative = QAction('negative', self)
        set_negative.triggered.connect(self.negative)

        set_sepia = QAction('sepia', self)
        set_sepia.triggered.connect(self.sepia)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Файл')
        fileMenu.addAction(openFile)
        fileMenu.addAction(set_bw)
        fileMenu.addAction(set_gray)
        fileMenu.addAction(set_negative)
        fileMenu.addAction(set_sepia)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def showDialog(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        pixmap = QPixmap(self.fname)
        self.lbl.resize(300, 300)
        self.lbl.setPixmap(pixmap)
        print(self.fname)
        return pixmap

    def bw(self):

        if self.fname:
            image = Image.open(self.fname)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()

            factor = 50
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    S = a + b + c
                    if (S > (((255 + factor) // 2) * 3)):
                        a, b, c = 255, 255, 255
                    else:
                        a, b, c = 0, 0, 0
                    draw.point((i, j), (a, b, c))

            img_tmp = ImageQt(image.convert('RGBA'))

            pixmap = QPixmap.fromImage(img_tmp)
            self.lbl.resize(300, 300)
            self.lbl.setPixmap(pixmap)
        else:
            self.showDialog()
            self.bw()

    def gray(self):
        if self.fname:
            image = Image.open(self.fname)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()

            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    S = (a + b + c) // 3
                    draw.point((i, j), (S, S, S))

            img_tmp = ImageQt(image.convert('RGBA'))

            pixmap = QPixmap.fromImage(img_tmp)

            self.lbl.resize(300, 300)
            self.lbl.setPixmap(pixmap)
        else:
            self.showDialog()
            self.bw()

    def negative(self):

        if self.fname:
            image = Image.open(self.fname)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()

            depth = 30
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    draw.point((i, j), (255 - a, 255 - b, 255 - c))

            img_tmp = ImageQt(image.convert('RGBA'))

            pixmap = QPixmap.fromImage(img_tmp)

            self.lbl.resize(300, 300)
            self.lbl.setPixmap(pixmap)
        else:
            self.showDialog()
            self.bw()

    def sepia(self):

        if self.fname:
            image = Image.open(self.fname)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()

            depth = 30
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    S = (a + b + c)
                    a = S + depth * 2
                    b = S + depth
                    c = S
                    if (a > 255):
                        a = 255
                    if (b > 255):
                        b = 255
                    if (c > 255):
                        c = 255
                    draw.point((i, j), (a, b, c))

            img_tmp = ImageQt(image.convert('RGBA'))

            pixmap = QPixmap.fromImage(img_tmp)

            self.lbl.resize(300, 300)
            self.lbl.setPixmap(pixmap)
        else:
            self.showDialog()
            self.bw()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
