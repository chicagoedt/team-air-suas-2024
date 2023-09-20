'''
    Enter an HSV color, show it visually
'''
import cv2
import numpy as np

color = [44, 100, 70]

colors = np.zeros((300, 300, 3), dtype = np.uint8)
height = len(colors)
width = len(colors[0])
for y in range(height):
    for x in range(width):
        colors[y][x][0] = color[0]
        colors[y][x][1] = color[1]
        colors[y][x][2] = color[2]

colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)
cv2.imshow('color', colors)
cv2.waitKey(0)
