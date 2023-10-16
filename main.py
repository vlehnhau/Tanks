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


class Player:
    def __init__(self, color, x, y):
        self.pLColor = color
        self.pLX = x
        self.pLY = y
        self.fuel = 100


    def move(self, direction):
        if self.fuel != 0:
            if direction == "RIGHT":
                if self.pLX != 1000-1:
                    self.pLX += 1
                    self.fuel -= 1
            if direction == "LEFT":
                if self.pLX != 1:
                    self.pLX -= 1
                    self.fuel -= 1





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

        ### Runden
        self.turn = "PL" #Links darf anfangen


        ### Player Left (grün)
        self.player_left = Player(QColor(0, 150, 0, 255),
                                  100,
                                  round(int((np.sin(2 * np.pi * 100 / 1000) * 0.5 + 1) * 400/2)))

        ### Player Right (red)
        self.player_right = Player(QColor(180, 0, 0, 255),
                                  900,
                                  round(int((np.sin(2 * np.pi * 900 / 1000) * 0.5 + 1) * 400 / 2)))



        self.mappainter = QPainter(self.world_img)
        # self.mappainter.setCompositionMode(QPainter.CompositionMode_Clear)
        self.mappainter.setPen(QColor(137, 207, 240, 255))
        self.mappainter.setBrush(QColor(137, 207, 240, 255))

        #Hiermit werden später die Krater gezeichnet
        #self.mappainter.drawEllipse(QPoint(60, 234), 50, 50)

        # timer
        self.timerFun()

        #Nur zum Testen ob checkGround funktion
        print(self.checkGround(10,10))      #False
        print(self.checkGround(500, 399))   #True
        print(self.checkGround(50,234))     #False
        print(self.checkGround(10,234))     #False
        print(self.checkGround(50, 285))    #True

        self.time = 0

    def onRepeat(self):
        # Erstellen eines temporären Bildes (Kopie von world_img)
        self.temp_img = QImage(self.world_img)

        # Einen QPainter für das temporäre Bild erstellen
        temppainter = QPainter(self.temp_img)

        # Player Left zeichnen
        temppainter.setPen(QColor(137, 207, 240, 255))
        temppainter.setBrush(self.player_left.pLColor)
        temppainter.drawRect(self.player_left.pLX-20, self.player_left.pLY, 40, -25)

        # Player Right zeichnen
        temppainter.setPen(QColor(137, 207, 240, 255))
        temppainter.setBrush(self.player_right.pLColor)
        temppainter.drawRect(self.player_right.pLX - 20, self.player_right.pLY, 40, -25)

        # Das temporäre Bild auf das Anzeigelabel setzen
        self.display.setPixmap(QPixmap.fromImage(self.temp_img))

        self.time += 1
        print(self.time)



    def timerFun(self):
        # timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(100)  # in milliseconds and controls the speed
        self.timer.timeout.connect(self.onRepeat)
        self.timer.start()


    def keyPressEvent(self, QKeyEvent):
        if self.turn == "PL":
            player = self.player_left
        elif self.turn == "PR":
            player = self.player_right
        else:
            pass

        if  QKeyEvent.key() == Qt.Key.Key_Right:
            player.move("RIGHT")
            self.fixY(player)
        elif QKeyEvent.key() == Qt.Key.Key_Left:
            player.move("LEFT")
            self.fixY(player)

        #Nächste Runde wenn "Space"
        elif QKeyEvent.key() == Qt.Key.Key_Space:
            if self.turn == "PL":
                self.player_right.fuel = 100
                self.turn = "PR"
            elif self.turn == "PR":
                self.player_left.fuel = 100
                self.turn = "PL"


    # Hier wird später ein Problem enstehen, wenn man versucht zu steile Kanten noch oben zu fahren.
    # Lösungen: Zählen wie oft man hoch geht. Wenn man z.B. mehr als 5 mal hoch muss, wieder zurück -> Geht nicht
    # Kann sein das dafür diese gesamte Funktion ganz anderes geschrieben werden muss

    # Panzer auf die richtige Höhe bringen
    def fixY(self, player):
        fixed = False
        if self.checkGround(player.pLX,player.pLY):   #Unterirdisch
            while fixed == False:
                player.pLY -=1
                if self.checkGround(player.pLX,player.pLY) == False:
                    player.pLY += 1
                    fixed = True
        else: #fliegt
            while fixed == False:
                player.pLY +=1
                if self.checkGround(player.pLX,player.pLY) == True:
                    fixed = True




    def checkGround(self, x, y):
        #Auffälligkeit: Wird ein Geschoss durch einen Panzer fliegen, wird das Geschoss trotzdem erst am Boden auftreffen
        pixel_value = self.world_img.pixel(x,y)
        color = QColor(pixel_value)
        if color == QColor(128, 128, 128, 255):
            return True
        else:
            return False




app = QApplication(sys.argv)

win = Window()
win.show()

app.exec()