'''
    input lower and upper hsv range and it will display the color increasing from lower to upper
'''

import cv2
import numpy as np

lower = [13, 60, 40]
upper = [17, 149, 149]

for h in range(lower[0], upper[0] + 1, 1):
    for s in range(lower[1], upper[1] + 1, 20):
        for v in range(lower[2], upper[2] + 1, 20):
            color = np.array([h, s, v])
            colors = np.zeros((400, 400, 3), dtype = np.uint8)
            height = len(colors)
            width = len(colors[0])
            for y in range(height):
                for x in range(width):
                    colors[y][x][0] = color[0]
                    colors[y][x][1] = color[1]
                    colors[y][x][2] = color[2]

            colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)
            text = str(h) + ', ' + str(s) + ', ' + str(v)
            cv2.imshow('color', colors)
            print(text)
            cv2.waitKey(1)