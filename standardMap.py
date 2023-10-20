import random
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QApplication
import sys

# Größe der Fläche
width = 1000
height = 600

# Erstellen eines leeren 2D Numpy-Arrays mit den Dimensionen width x height und 3 Kanälen (RGB)
world = np.zeros((height, width, 4), dtype=np.uint8)

# Erstellen einer Sinuskurve
w = np.linspace(0.001,0.05,20)

x_vals = np.arange(width)
y_vals = 0 #np.sin(2* np.pi * x_vals / width) * 0.3  # Sinuskurve

for i in w:
    y_vals = y_vals + (1/np.sqrt(i)*np.sin(i*x_vals + random.uniform(0, 2*np.pi))*random.uniform(-1,1)) * 0.009

# Schleife über die Pixel und setzen der Farben entsprechend der Sinuskurve
for x in range(width):
    for y in range(height):
        if y <= round(int((y_vals[x] + 1) * height/2) + 75):
            if y < 350 + random.randint(0,20) and y >= round(int((y_vals[x] + 1) * height / 2) + 60):
                world[y, x] = [255, 255, 255, 255]
            elif y >= round(int((y_vals[x] + 1) * height / 2) + 60 + random.randint(2,8)):
                world[y, x] = [0, 200, 0, 255]

            pass #world[y, x] = [137, 207, 240, 100]  # Blau für Punkte oberhalb der Sinuskurve
        else:
            if y-round(int((y_vals[x] + 1) * height/2) + 75)<50:
                world[y, x] = [128, 128, 128, 255]  # Grau für Punkte unterhalb der Sinuskurve
            elif y-round(int((y_vals[x] + 1) * height/2) + 75)<75:
                world[y, x] = [100, 100, 100, 255]
            elif y-round(int((y_vals[x] + 1) * height/2) + 75)<80:
                world[y, x] = [90, 90, 90, 255]
            elif y-round(int((y_vals[x] + 1) * height/2) + 75)<85:
                world[y, x] = [85, 85, 85, 255]
            elif y-round(int((y_vals[x] + 1) * height/2) + 75)<87:
                world[y, x] = [80, 80, 80, 255]
            elif y-round(int((y_vals[x] + 1) * height/2) + 75)<90:
                world[y, x] = [75, 75, 75, 255]
            elif y-round(int((y_vals[x] + 1) * height/2) + 75)<91:
                world[y, x] = [70, 70, 70, 255]
            elif y-round(int((y_vals[x] + 1) * height/2) + 75)<92:
                world[y, x] = [60, 60, 60, 255]
            else:
                rdmC = random.randint(1, 5)
                if rdmC == 1:
                    world[y, x] = [0, 0, 0, 255]
                elif rdmC == 2:
                    world[y, x] = [25, 25, 25, 255]
                elif rdmC == 3:
                    world[y, x] = [15, 15, 15, 255]
                elif rdmC == 4:
                    world[y, x] = [20, 20, 20, 255]
                elif rdmC == 5:
                    world[y, x] = [30, 30, 30, 255]


# Konvertiere das 2D Numpy-Array in ein QImage
# world_img = QImage(world.data, width, height, QImage.Format_RGB888)

def worldData():
    return world
