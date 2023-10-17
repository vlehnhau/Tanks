import random
import math
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
    def __init__(self, color, x, y, ang):
        self.pLColor = color
        self.pX = x
        self.pY = y
        self.fuel = 100
        self.angle = ang
        self.health = 1000
        self.power = 0

    # Bewegung des Spielers. Man kann nicht über den Rand hinaus fahren
    def move(self, direction):
        if self.fuel != 0:
            if direction == "RIGHT":
                if self.pX != 1000-21:
                    self.pX += 1
                    self.fuel -= 1
            if direction == "LEFT":
                if self.pX != 21:
                    self.pX -= 1
                    self.fuel -= 1

    # Winkel ändern
    def changeAngle(self, direction):
        if direction == "RIGHT":
            self.angle += 1
        if direction == "LEFT":
            self.angle -= 1

class Shot:
    def __init__(self):
        self.sX = 500       #Schuss startet irgendwo wo man ihn nicht sieht
        self.sY = 2000
        self.shot_angle = 0
        self.shot_power = 0
        self.flies = False




class Window(QWidget, object):
    def __init__(self):
        super().__init__()
        super().__init__()

        # timer
        self.timer = QTimer()

        # window settings
        self.setGeometry(450, 250, 1000, 600)
        self.setWindowTitle("Game")

        self.form = QFormLayout()  # Layout

        # create board
        self.board = QtGui.QPixmap(1000, 600)


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
        self.world_img = QImage(self.world.data, 1000, 600, QImage.Format_RGBA8888)

        ### Runden
        self.turn = "PL" #Links darf anfangen


        ### Player Left (grün)
        self.player_left = Player(QColor(0, 150, 0, 255),
                                  100,
                                  round(int((np.sin(2 * np.pi * 100 / 1000) * 0.3 + 1) * 600/2)+75),
                                  -45)

        ### Player Right (red)
        self.player_right = Player(QColor(200, 0, 0, 255),
                                  900,
                                  round(int((np.sin(2 * np.pi * 900 / 1000) * 0.3 + 1) * 600/2)+75),
                                  -135)


        ### Schuss (Wir benutzen immer wieder den selben Schuss)
        self.current_shoot = Shot()



        self.mappainter = QPainter(self.world_img)
        # self.mappainter.setCompositionMode(QPainter.CompositionMode_Clear)
        self.mappainter.setPen(QColor(137, 207, 240, 255))
        self.mappainter.setBrush(QColor(137, 207, 240, 255))

        #Hiermit werden später die Krater gezeichnet
        #self.mappainter.drawEllipse(QPoint(60, 434), 50, 50)


        # timer
        self.timerFun()
        self.time = 0

        self.spacepressed = False

    def timerFun(self):
        # timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(20)  # in milliseconds and controls the speed
        self.timer.timeout.connect(self.onRepeat)
        self.timer.start()


    def keyPressEvent(self, QKeyEvent):
        if self.turn == "PL":
            player = self.player_left
        elif self.turn == "PR":
            player = self.player_right
        else:
            pass

        # Spieler bewegen falls möglich
        if  QKeyEvent.key() == Qt.Key.Key_Right:
            if self.checkIfMovePossible(player.pX+1, player.pY):
                player.move("RIGHT")
                self.fixY(player)
        elif QKeyEvent.key() == Qt.Key.Key_Left:
            if self.checkIfMovePossible(player.pX-1, player.pY):
                player.move("LEFT")
                self.fixY(player)

        # angle ändern (Taste UP = Rechts, Taste Down = Links (Wie Blinker))
        elif QKeyEvent.key() == Qt.Key_Up:
            player.changeAngle("RIGHT")
        elif QKeyEvent.key() == Qt.Key_Down:
            player.changeAngle("LEFT")


        # Nächste Runde wenn "Space" (später schießen)
        elif QKeyEvent.key() == Qt.Key.Key_Space:
            if self.spacepressed == True and self.current_shoot.flies == False:
                if self.turn == "PL":

                    # Der Spieler schießt
                    self.shoot(self.player_left)

                    # self.player_right.fuel = 100
                    # self.player_right.power = 0
                    # self.turn = "PR"
                elif self.turn == "PR":
                    self.shoot(self.player_right)

                    # self.player_left.fuel = 100
                    # self.player_left.power = 0
                    # self.turn = "PL"
                self.spacepressed = False
            elif self.current_shoot.flies == False:
                self.spacepressed = True


    # Dadurch kann man nichtmehr zu Steile Kanten hoch- oder runterfahren
    def checkIfMovePossible(self,x,y):                #Man kann nicht hochfahren, wenn zu Nah über einen Boden ist
        if self.current_shoot.flies == False:         #Man kann nicht fahren, wenn man schon geschossen hat
            if (self.checkGround(x,y-25) == True):
                return False
            if (self.checkGround(x,y) == True):           #Man will hoch fahren
                if (self.checkGround(x,y-4) == True):
                    return False
                else:
                    return True

            elif (self.checkGround(x,y) == False):        #Man will runter fahren
                if (self.checkGround(x,y+4) == True):
                    return True
                else:
                    return False


    def shoot(self, player):
        if player == self.player_left:
            print("PL hat geschossen")
        else:
            print("PR hat geschossen")
        self.current_shoot.sX, self.current_shoot.sY = player.pX-2, player.pY-15 #Von hier aus fängt der schuss an zu fliegen
        self.current_shoot.shot_angle = player.angle
        self.current_shoot.shot_power = player.power
        self.current_shoot.flies = True





    # Panzer auf die richtige Höhe bringen
    def fixY(self, player):
        fixed = False
        if self.checkGround(player.pX,player.pY):   # Unterirdisch
            while fixed == False:
                player.pY -=1
                if self.checkGround(player.pX,player.pY) == False:
                    player.pY += 1
                    fixed = True
        else: # fliegt
            while fixed == False:
                player.pY +=1
                if self.checkGround(player.pX,player.pY) == True:
                    fixed = True




    def checkGround(self, x, y):
        # Auffälligkeit: Wird ein Geschoss durch einen Panzer fliegen, wird das Geschoss trotzdem erst am Boden auftreffen
        # Aber ist ein Feature, kein Bug
        pixel_value = self.world_img.pixel(x,y)
        color = QColor(pixel_value)
        if color == QColor(128, 128, 128, 255):
            return True
        else:
            return False


    def moveShot(self):
        # Gravitational constant (in pixel per frame squared)
        # Gravitational constant (in pixel per frame squared)
        g = 0.01

        if self.current_shoot.flies:
            # Berechne die horizontale Komponente der Schusskraft
            horizontal_force = (self.current_shoot.shot_power/4) * math.cos(
                math.radians(- self.current_shoot.shot_angle))

            # Berechne die vertikale Komponente der Schusskraft
            vertical_force = (self.current_shoot.shot_power/4) * math.sin(math.radians(- self.current_shoot.shot_angle))

            # Aktualisiere die vertikale Position (y) unter Berücksichtigung der Schwerkraft
            self.current_shoot.sY -= round(vertical_force - 0.5 * g * (self.time ** 2)/2)

            # Aktualisiere die horizontale Position (x) unter Verwendung der horizontalen Schusskraft
            self.current_shoot.sX += round(horizontal_force)

            # Aktualisiere die Zeit (für die parabolische Bewegung)
            self.time += 1

            if self.checkGround(self.current_shoot.sX, self.current_shoot.sY):
                self.current_shoot.flies = False
                self.shotHitGround()
            elif self.current_shoot.sX <= 0 or self.current_shoot.sX >= 1000:
                self.current_shoot.flies = False
                self.shootOutOfWorld()


    def shotHitGround(self):
        print("Treffer")
        self.mappainter.drawEllipse(self.current_shoot.sX-25,self.current_shoot.sY-35, 50, 50)
        if self.turn == "PL":
            self.player_right.fuel = 100
            self.player_right.power = 0
            self.time = 0
            self.current_shoot.sX, self.current_shoot.sY = 500,2000
            self.turn = "PR"

        elif self.turn == "PR":
            self.player_left.fuel = 100
            self.player_left.power = 0
            self.time = 0
            self.current_shoot.sX, self.current_shoot.sY = 500,2000
            self.turn = "PL"





    def shootOutOfWorld(self):
        if self.turn == "PL":
            self.player_right.fuel = 100
            self.player_right.power = 0
            self.time = 0
            self.current_shoot.sX, self.current_shoot.sY = self.player_right.pX - 2, self.player_right.pY - 15
            self.turn = "PR"

        elif self.turn == "PR":
            self.player_left.fuel = 100
            self.player_left.power = 0
            self.time = 0
            self.current_shoot.sX, self.current_shoot.sY = self.player_left.pX - 2, self.player_left.pY - 15
            self.turn = "PL"



    def onRepeat(self):
        # Power erhöhen, wenn Space gedrückt wurde
        if self.spacepressed == True:
            if self.turn == "PL":
                if self.player_left.power != 100:
                    self.player_left.power += 1
            if self.turn == "PR":
                if self.player_right.power != 100:
                    self.player_right.power += 1

        if self.current_shoot.flies == True:
            self.moveShot()




        # temporäres Bild (Kopie von world_img)
        self.temp_img = QImage(self.world_img)

        # Painter für temp
        temppainter = QPainter(self.temp_img)

        # Schuss
        temppainter.setBrush(Qt.black)
        temppainter.drawEllipse(self.current_shoot.sX, self.current_shoot.sY, 5, 5)


        # Player Left zeichnen
        temppainter.setPen(Qt.black)
        temppainter.setBrush(self.player_left.pLColor)
        temppainter.drawRect(self.player_left.pX-20, self.player_left.pY, 40, -25)

        ### Rohr zeichen (Player Left)
        # Um diesen Punkt rotiert sich das Rohr
        fixed_x, fixed_y = self.player_left.pX , self.player_left.pY -12.5

        temppainter.setBrush(QColor(0, 90, 0, 255))

        # Rotation
        transform = QTransform()
        transform.translate(fixed_x, fixed_y)
        temppainter.setTransform(transform)
        transform.rotate(self.player_left.angle)
        temppainter.setTransform(transform)

        # Rohr
        temppainter.drawRect(0, -2, 30, 5)
        # kleiner Zipfel am Rohr
        temppainter.drawRect(21, -4, 9, 9)
        # Transformation wieder zurück setzten
        temppainter.resetTransform()



        # Player Right zeichnen
        temppainter.setBrush(self.player_right.pLColor)
        temppainter.drawRect(self.player_right.pX - 20, self.player_right.pY, 40, -25)

        ### Rohr zeichen (Player Right)
        # Um diesen Punkt rotiert sich das Rohr
        fixed_x, fixed_y = self.player_right.pX, self.player_right.pY - 12.5
        temppainter.setBrush(QColor(120, 0, 0, 255))
        # Rotation
        transform = QTransform()
        transform.translate(fixed_x, fixed_y)
        temppainter.setTransform(transform)
        transform.rotate(self.player_right.angle)
        temppainter.setTransform(transform)
        # Rohr
        temppainter.drawRect(0, -2, 30, 5)
        # kleiner Zipfel am Rohr
        temppainter.drawRect(21, -4, 9, 9)
        # Transformation wieder zurück setzten
        temppainter.resetTransform()


        # Healthbar (Player Left)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(5,5,202,12)
        temppainter.setBrush(self.player_left.pLColor)
        temppainter.drawRect(6, 6, round(self.player_left.health/5), 10)
        # Healthbar (Player Right)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(793,5,202,12)
        temppainter.setBrush(self.player_right.pLColor)
        # Healthbar muss um 180° Rotiert werden
        fixed_x, fixed_y = (994, 6)
        transform = QTransform()
        transform.translate(fixed_x, fixed_y)
        temppainter.setTransform(transform)
        transform.rotate(180)
        temppainter.setTransform(transform)
        temppainter.drawRect(0, -10, round(self.player_right.health/5), 10)
        temppainter.resetTransform()

        # Power Bar (Player Left)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(5, 20, 152, 12)
        temppainter.setBrush(Qt.blue)
        temppainter.drawRect(6, 21, round(self.player_left.power * 1.5), 10)
         # Power Bar (Player Right)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(843, 21, 152, 12)
        fixed_x, fixed_y = (994,21)
        transform = QTransform()
        transform.translate(fixed_x, fixed_y)
        temppainter.setTransform(transform)
        transform.rotate(180)
        temppainter.setTransform(transform)
        temppainter.setBrush(Qt.blue)
        temppainter.drawRect(0, -11, round(self.player_right.power * 1.5), 10)
        temppainter.resetTransform()


        # Fuel Bar (Player Left)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(5, 35, 102, 12)
        temppainter.setBrush(Qt.darkYellow)
        temppainter.drawRect(6, 36, round(self.player_left.fuel * 1), 10)
        # Fuel Bar (Player Right)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(893, 36, 102, 12)
        fixed_x, fixed_y = (994, 36)
        transform = QTransform()
        transform.translate(fixed_x, fixed_y)
        temppainter.setTransform(transform)
        transform.rotate(180)
        temppainter.setTransform(transform)
        temppainter.setBrush(Qt.darkYellow)
        temppainter.drawRect(0, -11, round(self.player_right.fuel * 1), 10)
        temppainter.resetTransform()



        # temp zeichnen
        self.display.setPixmap(QPixmap.fromImage(self.temp_img))



app = QApplication(sys.argv)

win = Window()
win.show()

app.exec()



## Next Steps:
# Krater sind verbuggt. Können unter der Erde sein (Bisher KP wie fix)
# Schaden (easy)
# Anzeige wer an der Reihe ist
#
#
#
## Später:
# KI-Gegner (+ Startbildschirm zum entscheiden Spieler vs Spieler || Spieler vs Bot
# Wind
# Partikeleffekte der Explosion
# Panzer schräg fahren
# Random Map
# Fluktuationen im Wind