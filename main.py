import random
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QTimer, QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QApplication, QFormLayout, QWidget, QCheckBox, QPushButton, QSlider, QLabel, QMainWindow, \
    QMenuBar, QStatusBar, QMenu, QMessageBox

class Game():
    pass

class Player():
    pass

class Window(QWidget, object):
    def __init__(self):
        super().__init__()
        super().__init__()

        # timer for repeat
        self.timer = QTimer()

        # Outer win settings
        self.setGeometry(10, 30, 100, 100)
        self.setWindowTitle("Game")

        self.form = QFormLayout()  # Layout

        # creat board
        board = QtGui.QPixmap(50, 50)
        board.fill(QColor(100, 100, 255))

        # Screen
        self.display = QLabel()

        # Widget und Layout hinzufügen
        self.form.addWidget(self.display)
        self.setLayout(self.form)

        # timer
        self.timerFun()

    def onRepeat(self):
        width, hight = 600, 400

        board = QtGui.QPixmap(120, 60)
        board.fill(QColor(0, 0, 255))

        img = board.toImage()

        scaledBoardImg = img.scaled(width, hight, Qt.AspectRatioMode.KeepAspectRatio)
        self.display.setPixmap(QPixmap.fromImage(scaledBoardImg))

    def timerFun(self):
        # timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(150)  # in milliseconds and controls the speed
        self.timer.timeout.connect(self.onRepeat)
        self.timer.start()




app = QApplication(sys.argv)

win = Window()
win.show()

app.exec()