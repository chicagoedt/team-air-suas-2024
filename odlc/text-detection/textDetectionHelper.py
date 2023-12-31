'''
    Helper functions for textDetection.

    Assume the inputed image has only one printed letter. detect the letter
'''

import cv2                          # for reading image and processing image
import easyocr                      # a pytorch model that detects text and letters
import imutils                      # for rotating image
import time                         # for TESTING

import tool_imgPreprocessing as prepr       # for image processing
from specialcase import *                   # for dealing with rotated targets

DEBUG = False
SHOW_IMAGE = True

# stdSize = 125, stdScaledWidth = 120, stdCropSize = 45
# input target img, get the right size to crop and size to scale up
def getScaleAndCrop(img, stdSize, stdScaledWidth, stdCropSize):
    if DEBUG: 
        print('>> Begin getScaleAndCrop:')

    height = img.shape[0]
    width = img.shape[1]

    # get cropSize and scaledWidth
    averageSize = int((height + width) / 2)
    cropSize = int(stdCropSize * averageSize / stdSize)
    scaledWidth = stdScaledWidth #int(stdScaledWidth * averageSize / stdSize)

    # special case
    if cropSize < stdCropSize:
        cropSize = stdCropSize
    if scaledWidth < cropSize:
        scaledWidth = cropSize
    if DEBUG:
        print(f'image has height: {height}, width: {width} -> We need cropSize: {cropSize}, scaledWidth: {scaledWidth}')
        print('>> End getScaleAndCrop')
    return scaledWidth, cropSize

# image preprocessing before passing to text detection code
def imgPreprocessing(img, newWidth, cropSize): 
    # crop to only letter
    centerCoords = (int(img.shape[1] / 2), int(img.shape[0] / 2))
    cropped = prepr.cropImage(img, centerCoords, cropSize, cropSize)

    # scale the cropped so its bigger
    croppedScale = prepr.scaleImg(cropped, newWidth)

    # some blur and gray scale which help increase accuracy
    croppedBlur = cv2.GaussianBlur(croppedScale, (3,3), 0.5)
    croppedGray = cv2.cvtColor(croppedBlur, cv2.COLOR_BGR2GRAY)
    return croppedGray

# generate a list of rotations
def listRotations(img, step):
    rotations_list = []
    for i in range(0, 360, step):
        rotatedImg = imutils.rotate(img, i)
        rotations_list.append((rotatedImg, i))
    return rotations_list 

# get results from list of rotations
def detectLetter(rotations_list, reader):
    result_list = []
    # pass all rotated versions to model and get results
    for rotation in rotations_list: 
        output = reader.readtext(rotation[0])
        # print(rotation[1]) # detected text     # for TESTING 
        # print(output) # angle                  # for TESTING 
        if len(output) != 0: # if it detects something from a rotated image
            if len(output[0][1]) == 1 and (output[0][1].isalpha() or output[0][1].isnumeric()) and output[0][2] >= 0.9:
                result = (output[0][0], output[0][1], round(output[0][2], 2), rotation[1], rotation[0])
                     #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image
                result_list.append(result)               
    
    return result_list
            #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image

# detect letter in img
def readImgDetectLetter(img, reader, step):
    # get a list of rotations
    rotations_list = listRotations(img, step)

    # detect letter
    result_list = detectLetter(rotations_list, reader)
    return result_list
        #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image

# detect letter in img
# with img preprocessing and deduce the easyocr list
def deepReadImgDetectLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step):
    if DEBUG: 
        print('>> Begin deepReadImgDetectLetter:')

    startTime = time.time()
    # get scaledWidth and cropSize b4 pass to imgPreprocessing()
    scaledWidth, cropSize = getScaleAndCrop(img, stdSize, stdScaledWidth, stdCropSize)
    
    # preprocess img
    preprocessed = imgPreprocessing(img, scaledWidth, cropSize)

    # detect letter
    result_list = readImgDetectLetter(preprocessed, reader, step) # list generated by easyocr
    narrow_list = narrowResultList(result_list)  # deduce the easyocr list
    
    # show results
    result_list = [i[1] for i in result_list] # simplify result_list for nicer print
    print('What easyocr gets:', result_list)
    print('What we deduce from results get by easyocr:', narrow_list)

    print('Time to read image:', time.time() - startTime, 'seconds')

    if DEBUG:
        print('>> End deepReadImgDetectLetter')

    # show original img and preprocessed img
    if SHOW_IMAGE:
        cv2.imshow('original', img)               
        cv2.imshow('preprocessed', preprocessed)  
        cv2.waitKey(0)                            

    return narrow_list
