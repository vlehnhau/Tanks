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

    def getCannonPoint(self):
        # Kanonenrohr-Länge
        cannon_length = 30
        cannon_angle = -self.angle

        # Berechnen Sie die X- und Y-Koordinaten des Endpunkts
        end_x = round(self.pX-2 + cannon_length * math.cos(math.radians(cannon_angle)))
        end_y = round(self.pY-15 - cannon_length * math.sin(math.radians(cannon_angle)))

        return end_x, end_y

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

        self.particle = False
        self.particlesX = []
        self.particlesY = []
        self.particleColor = []
        self.particleAngle = []
        self.particlePower = []
        self.particleFlying = []

        for i in range(0, 100):
            self.particlesX.append(0)
            self.particlesY.append(0)
            self.particleAngle.append(0)
            self.particlePower.append(0)
            self.particleFlying.append(False)

        self.display = QLabel()
        # self.display.setGeometry(QRect(0, 0, 1000, 400))
        self.display.setAutoFillBackground(True)
        palette = self.display.palette()
        palette.setColor(QPalette.Window, QColor(120, 180, 255))  # Set the background color to blue
        self.display.setPalette(palette)

        # Widget und Layout hinzufügen
        self.form.addWidget(self.display)
        self.setLayout(self.form)

        # world
        self.world  = standardMap.worldData()
        self.world_img = QImage(self.world.data, 1000, 600, QImage.Format_RGBA8888)

        ### Runden
        self.turn = "PL" #Links darf anfangen

        ### ki init
        #self.ki = True Ki Gegner
        self.kimove = 0
        self.kimoved = 0
        self.kishot = False
        self.ki_last_hit = -100000
        self.curPower = 0

        self.timeSafe = 0

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

        self.player_left.pY = 50
        self.player_right.pY = 50

        self.fixY(self.player_left)
        self.fixY(self.player_right)

        ### Schuss (Wir benutzen immer wieder den selben Schuss)
        self.current_shoot = Shot()

        ### Wind wird zufällig berechent
        self.wind = random.randint(-50, 50)
        print("Wind: " + str(self.wind))

        ### Wolke
        self.cloud1X, self.cloud1Y = 180, 40
        self.cloud2X, self.cloud2Y = 560, 120
        self.cloud3X, self.cloud3Y = 940, 70




        self.mappainter = QPainter(self.world_img)
        # self.mappainter.setCompositionMode(QPainter.CompositionMode_Clear)
        self.mappainter.setPen(QColor(120, 180, 255))                  #                QColor(137, 207, 240, 255)
        self.mappainter.setBrush(QColor(120, 180, 255))            # QColor(137, 207, 240, 255)

        #Hiermit werden später die Krater gezeichnet
        #self.mappainter.drawEllipse(QPoint(60, 434), 50, 50)


        # timer
        self.timerFun()
        self.time = 0

        self.spacepressed = False

    def kisettings(self, val):
        self.ki = val
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
        elif self.turn == "PR" and self.ki == False:
            player = self.player_right
        elif self.turn == "PR" and self.ki:         #ki stuff
            return None
        else:
            pass

        # Spieler bewegen falls möglich
        if  QKeyEvent.key() == Qt.Key.Key_Right:
            if self.checkIfMovePossible(player.pX+1, player.pY):
                if self.turn == "PL":   # Die Panzer können nicht einander vorbeifahren
                    playerdiff = self.player_right.pX + 1  - self.player_left.pX
                    if playerdiff > 45:
                        player.move("RIGHT")
                        self.fixY(player)
                else:
                    player.move("RIGHT")
                    self.fixY(player)
        elif QKeyEvent.key() == Qt.Key.Key_Left:
            if self.checkIfMovePossible(player.pX-1, player.pY):
                if self.turn == "PR":   # Die Panzer können nicht einander vorbeifahren
                    playerdiff = self.player_right.pX - self.player_left.pX - 1
                    if playerdiff > 45:
                        player.move("LEFT")
                        self.fixY(player)
                else:
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
    def checkIfMovePossible(self,x,y):
        if self.current_shoot.flies == False:         #Man kann nicht fahren, wenn man schon geschossen hat
            if (self.checkGround(x,y-25) == True):
                return False
            if self.turn == "PL":
                playerdiff = round(math.sqrt((self.player_left.pX + 1 - self.player_right.pX)**2 + ((self.player_left.pY - 12) - (self.player_right.pY - 12))**2))
                if playerdiff < 45:
                    return False
            elif self.turn == "PR":
                playerdiff = round(math.sqrt((self.player_left.pX - self.player_right.pX - 1)**2 + ((self.player_left.pY - 12) - (self.player_right.pY - 12))**2))
                if playerdiff < 45:
                    return False

            if (self.checkGround(x,y) == True):           #Man will hoch fahren
                if (self.checkGround(x,y-6) == True):
                    return False
                else:
                    return True

            elif (self.checkGround(x,y) == False):        #Man will runter fahren
                if (self.checkGround(x,y+6) == True):
                    return True
                else:
                    return False


    def shoot(self, player):
        if player == self.player_left:
            print("PL hat geschossen")
        else:
            print("PR hat geschossen")
        self.current_shoot.sX, self.current_shoot.sY = player.getCannonPoint()
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
        color = QColor(pixel_value)                     #75,70,60,0
        if color == QColor(128, 128, 128, 255) or color ==QColor(100,100,100,255) or color == QColor(90,90,90,255) or color == QColor(85, 85, 85, 255) or color == QColor(80, 80, 80, 255) or color == QColor(75,75,75,255) or color == QColor(70,70,70,255) or color == QColor(60,60,60,255) or color == QColor(1,1,1,255) or color == QColor(25, 25, 25, 255) or color == QColor(15, 15, 15, 255) or color == QColor(20, 20, 20, 255) or color == QColor(30,30,30,255):
            return True
        else:
            return False


    def moveShot(self):
        g = 0.005

        if self.current_shoot.flies:
            # Berechne die horizontale Komponente der Schusskraft (X- Koord)
            horizontal_force = (self.current_shoot.shot_power/4) * math.cos(
                math.radians(-self.current_shoot.shot_angle))

            # Berechne die vertikale Komponente der Schusskraft (Y- Koord)
            vertical_force = (self.current_shoot.shot_power/4) * math.sin(math.radians(-self.current_shoot.shot_angle))

            # Aktualisiere die vertikale Position (y) -> (Verticalforce - Schwerkraft)
            self.current_shoot.sY -= round(vertical_force - (g * (self.time ** 2)/2))

            # Aktualisiere die horizontale Position (x) unter Verwendung der horizontalen Schusskraft (<-- +/- Wind)

            self.current_shoot.sX += round(horizontal_force + self.wind/20)


            # Aktualisiere die Zeit
            self.time += 1

            if self.checkGround(self.current_shoot.sX, self.current_shoot.sY):
                self.current_shoot.flies = False
                self.shotHitGround(self.current_shoot.sX, self.current_shoot.sY)
            elif self.current_shoot.sX <= 0 or self.current_shoot.sX >= 1000 or self.current_shoot.sY > 600:
                self.current_shoot.flies = False
                self.shootOutOfWorld()



    # Andere moveShot funktion ohne "Kraterbug". Aber irgendwie ist dauerhaft Player Left dran, verstehe nicht wieso
    # def moveShot(self):
    #     # Gravitational constant
    #     g = 0.005
    #
    #     if self.current_shoot.flies:
    #         # Berechne die horizontale Komponente der Schusskraft (X- Koord)
    #         horizontal_force = (self.current_shoot.shot_power/4) * math.cos(
    #             math.radians(-self.current_shoot.shot_angle))
    #
    #         # Berechne die vertikale Komponente der Schusskraft (Y- Koord)
    #         vertical_force = (self.current_shoot.shot_power/4) * math.sin(math.radians(-self.current_shoot.shot_angle))
    #
    #         # Aktualisiere die vertikale Position (y) -> (Verticalforce - Schwerkraft)
    #         Yshift = round(vertical_force - (g * (self.time ** 2)/2))
    #
    #         # Aktualisiere die horizontale Position (x) unter Verwendung der horizontalen Schusskraft (<-- +/- Wind)
    #
    #         Xshift = round(horizontal_force + self.wind/20)
    #         foundGround = False
    #
    #
    #         for i in range(1,101):
    #             if self.checkGround(round(self.current_shoot.sX + i/100 * Xshift), round(self.current_shoot.sY - i/100 * Yshift)) and foundGround == False:
    #                 foundGround = True
    #                 self.current_shoot.flies = False
    #                 self.current_shoot.sX += round(i/100 * Xshift)
    #                 self.current_shoot.sY -= round(i/100 * Yshift)
    #                 self.current_shoot.flies = False
    #                 self.shotHitGround(self.current_shoot.sX, self.current_shoot.sY)
    #
    #         if foundGround == False:
    #             self.current_shoot.sX += Xshift
    #             self.current_shoot.sY -= Yshift
    #
    #         self.time += 1
    #
    #
    #
    #         if self.current_shoot.sX <= 0 or self.current_shoot.sX >= 1000 or self.current_shoot.sY > 600:
    #             self.current_shoot.flies = False
    #             self.shootOutOfWorld()

    def doparticle(self):
        g = 0.005
        self.timeSafe += 1

        for i in range(0, 50):
            if self.particleFlying[i] != False:

                horizontal_force = (self.particlePower[i] / 4) * math.cos(
                    math.radians(-self.particleAngle[i]))

                # Berechne die vertikale Komponente der Schusskraft (Y- Koord)
                vertical_force = (self.particlePower[i] / 4) * math.sin(
                    math.radians(-self.particleAngle[i]))

                # Aktualisiere die vertikale Position (y) -> (Verticalforce - Schwerkraft)
                self.particlesY[i] = self.particlesY[i] - round(vertical_force - (g * (self.timeSafe ** 2) / 2))
                # Aktualisiere die horizontale Position (x) unter Verwendung der horizontalen Schusskraft (<-- +/- Wind)

                self.particlesX[i] += round(horizontal_force + self.wind / 20)



            if self.checkGround(self.particlesX[i], self.particlesY[i]):
                self.particleFlying[i] = False
                counter = 0
                for i in range(0, 50):
                    if self.particleFlying[i]:
                        counter = counter + 1

                if counter >= 95:
                    self.particle = False
                    self.timeSafe = 0

            # elif self.current_shoot.sX <= 0 or self.current_shoot.sX >= 1000 or self.current_shoot.sY > 600:
            #     self.current_shoot.flies = False
            #     self.shootOutOfWorld()


    def shotHitGround(self, x, y):
        print("Treffer")
        pixel_value = self.world_img.pixel(x, y)
        color = QColor(pixel_value)
        if color == QColor(1, 1, 1, 255) or color == QColor(25, 25, 25, 255) or color == QColor(15, 15, 15, 255) or color == QColor(20, 20, 20, 255) or color == QColor(30,30,30,255):
            pass
        else:
            self.mappainter.drawEllipse(self.current_shoot.sX-25,self.current_shoot.sY-40, 50, 50)
            self.fixY(self.player_left)
            self.fixY(self.player_right)

        self.particle = True
        for i in range(0, 50):
            self.particlesX[i] = x + random.randint(-15, 15)
            self.particlesY[i] = y + random.randint(-15 , 15)
            self.particleAngle[i] = random.randint(220,300)
            self.particlePower[i] = random.randint(2,20)
            self.particleFlying[i] = True


        # Schaden berechnen:
        self.calcDMG()
        if self.turn == "PL":
            self.player_right.fuel = 100
            self.player_right.power = 0
            self.time = 0
            self.timeSafe = 0
            self.current_shoot.sX, self.current_shoot.sY = 500, 2000
            self.turn = "PR"
            self.wind = random.randint(-50, 50)
            print("Wind: " + str(self.wind))

        elif self.turn == "PR":
            if self.ki:
                self.ki_last_hit = self.current_shoot.sX
            self.player_left.fuel = 100
            self.player_left.power = 0
            self.time = 0
            self.timeSafe = 0
            self.current_shoot.sX, self.current_shoot.sY = 500,2000
            self.turn = "PL"
            self.wind = random.randint(-50, 50)
            print("Wind: " + str(self.wind))

    def calcDMG(self):
        # Schaden von Player Left
        diff = round(math.sqrt((self.current_shoot.sX - self.player_left.pX)**2 + (self.current_shoot.sY - (self.player_left.pY - 15))**2))
        # Radius des Schusses: 25 | Breite des Panzers/2 = 20 | Treffer bei Diff < 45
        if diff < 45:
            self.player_left.health -= 100 + (45-diff) * 5

        # Schaden von Player Right
        diff = round(math.sqrt((self.current_shoot.sX - self.player_right.pX)**2 + (self.current_shoot.sY - (self.player_right.pY - 15))**2))
        # Radius des Schusses: 25 | Breite des Panzers/2 = 20 | Treffer bei Diff < 45
        if diff < 45:
            self.player_right.health -= 100 + (45-diff) * 5



    def shootOutOfWorld(self):
        self.wind = random.randint(-50, 50)
        if self.turn == "PL":
            self.player_right.fuel = 100
            self.player_right.power = 0
            self.time = 0
            self.timeSafe =0
            self.current_shoot.sX, self.current_shoot.sY = 500,2000
            self.turn = "PR"

        elif self.turn == "PR":
            self.player_left.fuel = 100
            self.player_left.power = 0
            self.time = 0
            self.timeSafe = 0
            self.current_shoot.sX, self.current_shoot.sY = 500,2000
            self.turn = "PL"



    def onRepeat(self):
        # Power erhöhen, wenn Space gedrückt wurde
        if self.spacepressed == True:
            if self.turn == "PL":
                if self.player_left.power != 60:
                    self.player_left.power += 1
                else:
                    self.player_left.power = 0
            if self.turn == "PR":
                if self.player_right.power != 60:
                    self.player_right.power += 1
                else:
                    self.player_right.power = 0

        if self.current_shoot.flies == True:
            self.moveShot()

        if self.particle:
            self.doparticle()

        # temporäres Bild (Kopie von world_img)
        self.temp_img = QImage(self.world_img)

        # Painter für temp
        temppainter = QPainter(self.temp_img)


        ### Wolke
        temppainter.setPen(Qt.white)
        temppainter.setBrush(Qt.white)
        # Bewegung der Wolke 1
        self.cloud1X = round(self.cloud1X + self.wind/10)
        if self.cloud1X < 0 -25:
            self.cloud1X = 1000 + 150
        if self.cloud1X > 1000 + 150:
                self.cloud1X = 0 - 25
        #Zeichnen der Wolke 1
        temppainter.drawEllipse(self.cloud1X - 25, self.cloud1Y, 50, 50)                            # ganz rechts
        temppainter.drawEllipse(self.cloud1X - 35 - 15, self.cloud1Y - 15, 50, 50)
        temppainter.drawEllipse(self.cloud1X - 25 - 15 - 25, self.cloud1Y - 15 - 10, 50, 50)
        temppainter.drawEllipse(self.cloud1X - 25 - 15 - 25 - 20, self.cloud1Y - 15 + 20, 50, 50)   # ganz links
        temppainter.drawEllipse(self.cloud1X - 25 - 15 - 25 + 10, self.cloud1Y - 15 + 17, 50, 50)

        # Bewegung der Wolke 2
        self.cloud2X = round(self.cloud2X + self.wind / 10)
        if self.cloud2X < 0 - 25:
            self.cloud2X = 1000 + 150
        if self.cloud2X > 1000 + 150:
            self.cloud2X = 0 - 25
        # Zeichnen der Wolke 2
        temppainter.drawEllipse(self.cloud2X - 20, self.cloud2Y, 40, 40)            # ganz rechts
        temppainter.drawEllipse(self.cloud2X - 20 - 50, self.cloud2Y - 25, 60, 60)
        temppainter.drawEllipse(self.cloud2X - 20 - 85, self.cloud2Y - 10, 50, 50)  # ganz links
        temppainter.drawEllipse(self.cloud2X - 20 - 55, self.cloud2Y + 10, 40, 40)
        temppainter.drawEllipse(self.cloud2X - 20 - 30, self.cloud2Y + 5, 40, 40)



        # Bewegung der Wolke 3
        self.cloud3X = round(self.cloud3X + self.wind / 10)
        if self.cloud3X < 0 - 25:
            self.cloud3X = 1000 + 150
        if self.cloud3X > 1000 + 150:
            self.cloud3X = 0 - 25
        # Zeichnen der Wolke 3
        temppainter.drawEllipse(self.cloud3X - 10, self.cloud3Y - 5, 20, 20)        # ganz rechts
        temppainter.drawEllipse(self.cloud3X - 10 - 10, self.cloud3Y - 17, 20, 20)
        temppainter.drawEllipse(self.cloud3X - 10 - 35, self.cloud3Y - 25, 30, 30)
        temppainter.drawEllipse(self.cloud3X - 10 - 60, self.cloud3Y - 15, 34, 34) # ganz links
        temppainter.drawEllipse(self.cloud3X - 10 - 45, self.cloud3Y, 35, 35)
        temppainter.drawEllipse(self.cloud3X - 10 - 25, self.cloud3Y - 5, 35, 35)



        # Schuss
        temppainter.setPen(Qt.black)
        temppainter.setBrush(Qt.black)
        temppainter.drawEllipse(self.current_shoot.sX, self.current_shoot.sY, 5, 5)

        # Particle
        if self.particle:
            for i in range(0, 50):
                if self.particleFlying[i]:
                    karl = random.randint(1, 6)
                    color = Qt.red
                    if karl == 1:
                        color = Qt.yellow
                    elif karl == 2:
                        color = QColor(255, 20, 20, 255)
                    elif karl == 3:
                        color = QColor(255, 200, 20, 255)
                    elif karl == 4:
                        color = QColor(245, 93, 12, 255)
                    elif karl == 5:
                        color = QColor(200, 20, 14, 255)

                    temppainter.setPen(color)
                    temppainter.setBrush(color)
                    temppainter.drawEllipse(self.particlesX[i], self.particlesY[i], 4, 4)

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

        # Power Bar (Player Left)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(5, 20, 152, 12)
        temppainter.setBrush(Qt.blue)
        temppainter.drawRect(6, 21, round(self.player_left.power * 2.5), 10)
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
        temppainter.drawRect(0, -11, round(self.player_right.power * 2.5), 10)
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

        # Healthbar (Player Left)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(5, 5, 202, 12)
        temppainter.setBrush(self.player_left.pLColor)
        if self.player_left.health > 0:
            temppainter.drawRect(6, 6, round(self.player_left.health / 5), 10)
        else:  # Rot hat gewonnen
            print("Rot hat gewonnen")
            msg = QMessageBox()
            msg.setWindowTitle("GAME OVER")
            msg.setText("The winner is red")
            self.timer.stop()
            msg.exec()

        # Healthbar (Player Right)
        temppainter.setBrush(Qt.black)
        temppainter.drawRect(793, 5, 202, 12)
        temppainter.setBrush(self.player_right.pLColor)
        # Healthbar muss um 180° Rotiert werden
        fixed_x, fixed_y = (994, 6)
        transform = QTransform()
        transform.translate(fixed_x, fixed_y)
        temppainter.setTransform(transform)
        transform.rotate(180)
        temppainter.setTransform(transform)
        if self.player_right.health > 0:
            temppainter.drawRect(0, -10, round(self.player_right.health / 5), 10)
        else:   # Grün hat gewonnen
            print("Grün hat gewonnen")
            msg = QMessageBox()
            msg.setWindowTitle("GAME OVER")
            msg.setText("The winner is green")
            self.timer.stop()
            msg.exec()

        temppainter.resetTransform()

        # temp zeichnen
        self.display.setPixmap(QPixmap.fromImage(self.temp_img))

        if self.turn == "PR" and self.ki:
            self.do_ki()
        else:
            self.kimove = random.randint(20, 80)
            self.kishot = False
            self.kimoved = 0

    def do_ki(self):
        if self.kimoved <= self.kimove:
            if self.player_left.pX > self.player_right.pX + 30:
                if self.checkIfMovePossible(self.player_right.pX + 1, self.player_right.pY):
                    self.player_right.move("RIGHT")
                    self.fixY(self.player_right)

                self.kimoved = self.kimoved + 1
            elif self.player_left.pX + 30 < self.player_right.pX:
                if self.checkIfMovePossible(self.player_right.pX - 1, self.player_right.pY):
                    self.player_right.move("LEFT")
                    self.fixY(self.player_right)

                self.kimoved = self.kimoved + 1
            else:
                pass

        if self.kimove < self.kimoved and self.kishot == False:
            if self.ki_last_hit == -100000:
                self.player_right.angle = 240 + random.randint(-10,10)
                self.curPower = 50 + random.randint(-5,5)
                self.player_right.power = self.curPower
            elif self.player_left.pX - self.ki_last_hit > -10:                                            # Eintreffer rechts von Gegner
                self.player_right.angle = self.player_right.angle + 1#(1 + random.randint(1,2))
                self.player_right.power = self.curPower  #(1 + random.randint(1,2))
            elif self.player_left.pX - self.ki_last_hit < 10:                                             # Eintreffer links von Gegner
                self.player_right.angle = self.player_right.angle - 1#(1 + random.randint(1,2))
                self.player_right.power = self.curPower #(1 + random.randint(1,2))
            elif self.player_left.pX - self.ki_last_hit == 0:
                pass

            self.shoot(self.player_right)
            self.kishot = True

            print(self.player_left.pX - self.ki_last_hit)


class Ui_MainWindow(object):
    def __init__(self, winIn: Window):
        super().__init__()
        self.timer = QTimer()
        self.game = winIn

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(343, 321)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # button
        self.submitki = QPushButton(parent=self.centralwidget, clicked=self.submitKi, text="PvE")  # Button submit settings
        self.submitki.setGeometry(QRect(20, 130, 113, 32))
        self.submitki.setObjectName("submitPvE")

        self.submitPvP = QPushButton(parent=self.centralwidget, clicked=self.submitNoKi, text="PvP")  # Button submit settings
        self.submitPvP.setGeometry(QRect(200, 130, 113, 32))
        self.submitPvP.setObjectName("submitPvP")

        MainWindow.setCentralWidget(self.centralwidget)

    def submitNoKi(self):
        self.game.kisettings(False)
        self.game.show()
        MainWindow.close()
    def submitKi(self):
        self.game.kisettings(True)
        self.game.show()
        MainWindow.close()


app = QApplication(sys.argv)


win = Window()

MainWindow = QMainWindow()
ui = Ui_MainWindow(win)
ui.setupUi(MainWindow)
MainWindow.show()

app.exec()



## Viktor:
# KI                    -> do it later (vlt.)
# endscreen -> restart und wer hat gewonnen junge
#
## Mika:
# nicht durch wände     ->
# nicht mehr vorbeifahren
#
#
#
