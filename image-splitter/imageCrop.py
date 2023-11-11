import cv2
import os
#from shutil import rmtree

imagesDir = "/Users/ethanky/Documents/GitHub/team-air-suas-2024/image-splitter/myImages"
imgPath = "/Users/ethanky/Documents/GitHub/team-air-suas-2024/simulate-images/snapshots/target/img_001_tar_000.jpg"

targetSize = 100

def printSeveralImages(img, x, y, a, b):
    #Sets x and y (start and end) positions
    startx = x
    starty = y
    endx = 0
    endy = 0

    #Stores the dimensions of image
    maxWidth = len(img)
    maxHeight = len(img[0])

    #Iterates through startx and starty based on dimensions
    while starty < maxHeight:
        endy = starty + b
        while startx < maxWidth:
            endx = startx + a
            cropped_image = img[startx:endx, starty:endy]
            print(str(startx)+"-"+str(starty)+"-"+str(endx)+"-"+str(endy))
            cv2.imwrite(imagesDir+"/"+str(startx)+"-"+str(starty)+"-"+str(endx)+"-"+str(endy)+".jpg", cropped_image)
            #startx += a
            startx += (a - targetSize)
        #starty += b
        starty += (b - targetSize)
        startx = x

def printLayers(img, a, b):
    
    #if os.path.exists(imagesDir):
    #    os.remove(imagesDir)
    #    os.mkdir(imagesDir)

    # check if target directory exists
    #if os.path.exists(vars.targetDir):
    #    rmtree(vars.targetDir)
    printSeveralImages(img, 0,    0,    a, b)
    #printSeveralImages(img, a//2, 0,    a, b)
    #printSeveralImages(img, 0,    b//2, a, b)
    #printSeveralImages(img, a//2, b//2, a, b)

#Gets image given path
img = cv2.imread(imgPath)
print(img.shape)

printLayers(img, 640, 640)

#Crop image
#cropped_image = img[0:10, 0:10]
#cv2.imwrite("/Users/ethanky/Downloads/Personal stuff/OpenCVTest/myImages/cropped_image.jpg", cropped_image)


#cv2.imshow("EK", cropped_image)
#cv2.waitKey(0)