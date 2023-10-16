import random
import sys
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import standardMap

class Game():
    pass


class PlayerLeft():
    pLColor = QColor(0,150,0,255)
    pLX = 100
    pLY = round(int((np.sin(2 * np.pi * pLX / 1000) * 0.5 + 1) * 400/2)) - 25

class Window(QWidget, object):
    def __init__(self):
        super().__init__()
        super().__init__()

        # timer for repeat
        self.timer = QTimer()

        # Outer win settings
        self.setGeometry(10, 30, 1000, 400)
        self.setWindowTitle("Game")

        self.form = QFormLayout()  # Layout

        # create board
        self.board = QtGui.QPixmap(1000, 400)


        self.display = QLabel()
        # self.display.setGeometry(QRect(0, 0, 1000, 400))
        self.display.setAutoFillBackground(True)
        palette = self.display.palette()
        palette.setColor(QPalette.Window, QColor(137, 207, 240))  # Set the background color to blue
        self.display.setPalette(palette)

        # Widget und Layout hinzufügen
        self.form.addWidget(self.display)
        self.setLayout(self.form)

        # world
        self.world = standardMap.worldData()
        self.world_img = QImage(self.world.data, 1000, 400, QImage.Format_RGBA8888)

        self.mappainter = QPainter(self.world_img)
        # self.mappainter.setCompositionMode(QPainter.CompositionMode_Clear)
        self.mappainter.setPen(QColor(137, 207, 240, 255))
        self.mappainter.setBrush(QColor(137, 207, 240, 255))

        #Hiermit werden später die Krater gezeichnet
        #Maybe Problem: Panzer werden auch überzeichnet, aber man könnte ja die Panzer dann wieder darüber malen
        #self.mappainter.drawEllipse(QPoint(50, 234), 50, 50)

        #Test PlayerL
        self.mappainter.setBrush(PlayerLeft.pLColor)
        self.mappainter.drawRect(PlayerLeft.pLX-20, PlayerLeft.pLY, 40, 25)

        # timer
        self.timerFun()

        #Nur zum Testen der checkGround funktion
        print(self.checkHit(10,10))      #False
        print(self.checkHit(500, 399))   #True
        print(self.checkHit(50,234))     #False
        print(self.checkHit(10,234))     #False
        print(self.checkHit(50, 285))    #True

        #Test für Player
        print(PlayerLeft.pLX)
        print(PlayerLeft.pLY)

        self.kek = 0


    def onRepeat(self):
        img = self.board.toImage()

        self.display.setPixmap(QPixmap.fromImage(self.world_img))

        self.kek += 1
        print(self.kek)






    def timerFun(self):
        # timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(150)  # in milliseconds and controls the speed
        self.timer.timeout.connect(self.onRepeat)
        self.timer.start()



    def checkHit(self, x, y):
        #Funktion um zu Überprüfen, ob ein Pixel Boden oder Himmel ist.
        #ABER:
        #Maybe Problem in der Zukunft: Wenn ein Panzer den Boden Überdeckt, wird der Boden nicht mehr erkannt (da die Farbe des Pixel abgefragt wird)
        #Aber: juckt mich doch nicht, Viktor muss das mit den Panzern machen hehe
        #Maybe muss man anderes Bild drüber legen oder so, KP ob QLabel das kann
        #oder: if ... or color == Farbe Panzer
        pixel_value = self.world_img.pixel(x,y)
        color = QColor(pixel_value)
        if color == QColor(128, 128, 128, 255) or color == PlayerLeft.pLColor:
            return True
        else:
            return False




app = QApplication(sys.argv)

win = Window()
win.show()

app.exec()