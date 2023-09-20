'''
    
'''
import cv2
import os

# path to image
folder_path = ''
filename = ''
filePath = os.path.join(folder_path, filename)

# readImg, convert to HSV
img = cv2.imread(filePath)
img = cv2.resize(img, (300, 300))
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

print(img[18][45])