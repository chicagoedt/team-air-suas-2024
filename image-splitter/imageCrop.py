import cv2

def printSeveralImages(img, layer, x, y, a, b):
    startx = x
    starty = y
    endx = 0
    endy = 0

    maxWidth = len(img)
    maxHeight = len(img[0])

    i = 0
    j = 0
    while starty < maxHeight:
        endy = starty + b
        while startx < maxWidth:
            endx = startx + a
            cropped_image = img[startx:endx, starty:endy]
            cv2.imwrite("/Users/ethanky/Downloads/Personal stuff/OpenCVTest/myImages/cropped_image"+str(i)+":"+str(j)+":"+str(layer)+".jpg", cropped_image)
            startx += a
            i +=1
        starty += b
        j += 1
        startx = 0

def printLayers(img, a, b):
    printSeveralImages(img, 0, 0,    0,    a, b)
    printSeveralImages(img, 1, a//2, 0,    a, b)
    printSeveralImages(img, 2, 0,    b//2, a, b)
    printSeveralImages(img, 3, a//2, b//2, a, b)

#Gets image given path
imgPath = "/Users/ethanky/Downloads/Personal stuff/OpenCVTest/OG profile pic.jpeg"
img = cv2.imread(imgPath)
print(img.shape)

printLayers(img, 50, 50)

#Crop image
#cropped_image = img[0:10, 0:10]
#cv2.imwrite("/Users/ethanky/Downloads/Personal stuff/OpenCVTest/myImages/cropped_image.jpg", cropped_image)


#cv2.imshow("EK", cropped_image)
#cv2.waitKey(0)