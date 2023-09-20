'''
    Real life images can vary in light intensity (or light level)
    Functions that measure the light intensity (or light level) of runaway.
    From Light level, apply appropriate contrast and brightness change to image
'''

import numpy as np
import cv2

import tool_imgPreprocessing as prepr
import tool_colorFunc as colorFunc

# give a background image measure light level
def measureBackgroundLightLevel(img):
    print('>> in measureBackgroundLightLevel: measuring light level of image and estimate its average color')
    imgScaled = prepr.scaleImg(img, 30)
    # cv2.imshow('scaled', imgScaled)
    # cv2.waitKey(0)
    imgScaledHSV = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2HSV)
    height = imgScaled.shape[0]
    width = imgScaled.shape[1]
    
    # sum all pixels and get average
    numPixel = 0
    sumB = 0
    sumG = 0
    sumR = 0
    for y in range(height):
        for x in range(width):
            if not (colorFunc.hsvInRangeArray(imgScaledHSV[y][x], colorFunc.lowerWhite_array, colorFunc.upperWhite_array) or colorFunc.hsvInRangeArray(imgScaledHSV[y][x], colorFunc.lowerBlack_array, colorFunc.upperBlack_array)):
                numPixel += 1
                sumB += imgScaled[y][x][0]
                sumG += imgScaled[y][x][1]
                sumR += imgScaled[y][x][2]
    
    averageColor = np.array([[[int(sumB / numPixel), int(sumG / numPixel), int(sumR / numPixel)]]], dtype = np.uint8)
    averageColorHSV = cv2.cvtColor(averageColor, cv2.COLOR_BGR2HSV)

    # light level of the average is the V value
    lightLevel = averageColorHSV[0][0][2]
    
    # show output
    print('average color: {} -> averageHSV color: {}, light level: {}'.format(averageColor, averageColorHSV, lightLevel))
    print('>> end measureBackgroundLightLevel')
    return lightLevel

# get corresponding brightness change and contrast change depending on lightLevel
# to pass to function apply_brightness_contrast() in y_imgPreprocessing.py
def getBrightnessContrastChange(lightLevel):
    print('>> in getBrightnessContrastChange()')  
    brightnessChange = 0
    contrastChange = 0

    # light level table
    if 35 <= lightLevel and lightLevel <= 45:           # this is light level of real images in folder 15march
        brightnessChange = 82
        contrastChange = 95
    elif lightLevel < 70:                               # ???
        print('I do not recognize this light level')
        brightnessChange = 82
        contrastChange = 95
    elif 70 <= lightLevel and lightLevel <= 100:        # this is light level of the simulated image
        brightnessChange = 0
        contrastChange = 0
    elif lightLevel < 165:                              # ???
        print('I do not recognize this light level')
        brightnessChange = -105
        contrastChange = 95
    elif 165 <= lightLevel and lightLevel <= 180:       # this is light level of real images in folder 4march
        brightnessChange = -105
        contrastChange = 95
    else:                                               # ???
        print('I do not recognize this light level')
        brightnessChange = -105                         
        contrastChange = 95

    print('Light Level: {} -> Brightness change: {}, Contrast change: {}'.format(lightLevel, brightnessChange, contrastChange))
    print('>> Finish getBrightnessContrastChange()')
    return brightnessChange, contrastChange


