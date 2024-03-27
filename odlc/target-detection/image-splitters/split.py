'''
    Break a big images into smaller images of size a * b. 
    If the big image has size 4K then number of small images is 48.
'''

import cv2
import os
from shutil import rmtree

imagesDir = "./images" # the path where broken images are stored, just leave it by default
imgPath = "" # put the path to image that wants to be broken

maxTargetSize = 118

# dissect big image into small images size a * b, starting at coordinate (0, 0)
def splitImages(img, a, b):
    # Sets x and y (start and end) positions
    startx = 0
    starty = 0
    endx = 0
    endy = 0

    # Stores the dimensions of image
    maxWidth = len(img)
    maxHeight = len(img[0])

    # Iterates through startx and starty based on dimensions
    while starty < maxHeight:
        endy = starty + b
        while startx < maxWidth:
            endx = startx + a
            cropped_image = img[startx:endx, starty:endy]
            print(str(startx)+"-"+str(starty)+"-"+str(endx)+"-"+str(endy))
            cv2.imwrite(imagesDir+"/"+str(startx)+"-"+str(starty)+"-"+str(endx)+"-"+str(endy)+".jpg", cropped_image)
            startx += (a - maxTargetSize)

        starty += (b - maxTargetSize)
        startx = 0

if __name__ == "__main__":
    img = cv2.imread(imgPath)
    if os.path.exists(imagesDir):
        rmtree(imagesDir)
    os.makedirs(imagesDir)  
    splitImages(img, 640, 640)