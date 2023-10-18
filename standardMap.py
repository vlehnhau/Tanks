import numpy as np
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QApplication
import sys

# Größe der Fläche
width = 1000
height = 600

# Erstellen eines leeren 2D Numpy-Arrays mit den Dimensionen width x height und 3 Kanälen (RGB)
world = np.zeros((height, width, 4), dtype=np.uint8)

# Erstellen einer Sinuskurve
x_vals = np.arange(width)
y_vals = np.sin(2* np.pi * x_vals / width) * 0.3  # Sinuskurve

# Schleife über die Pixel und setzen der Farben entsprechend der Sinuskurve
for x in range(width):
    for y in range(height):
        if y <= round(int((y_vals[x] + 1) * height/2) + 75):
            pass #world[y, x] = [137, 207, 240, 100]  # Blau für Punkte oberhalb der Sinuskurve
        else:
            world[y, x] = [128, 128, 128, 255]  # Grau für Punkte unterhalb der Sinuskurve



# Konvertiere das 2D Numpy-Array in ein QImage
# world_img = QImage(world.data, width, height, QImage.Format_RGB888)

def worldData():
    return world

