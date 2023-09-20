'''
    extract color from image
'''
# Task: find the range for red
import os
import cv2
import numpy as np
import tool_colorFunc as colorFunc
import tool_adaptToRealLife as adapt
import tool_imgPreprocessing as prepr

def imgPreprocessing(img):
    lightLevel = adapt.measureBackgroundLightLevel(img)
    brightnessChange, contrastChange = adapt.getBrightnessContrastChange(lightLevel)
    print('brightnessChange: {}, contrastChange: {}'.format(brightnessChange, contrastChange))
    img = prepr.apply_brightness_contrast(img, brightnessChange, contrastChange)
    return img

folder_path = '/Users/mightymanh/Desktop/real images/march4'
filename = 'gray_sqaure_green_2_red_rectangle_yellow_1.jpg'

# path to image
# file_path = '/Users/mightymanh/Desktop/HSVrange.png'
file_path = os.path.join('/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023/object-detection/playWithColor/cropImages/white_octogon_black_2_green_pentagon_yellow_O_3210-1090_Green.jpg')
img = cv2.imread(file_path)

# # preprocess img
# preprocessed = imgPreprocessing(img)

# scale target so it's big enough
imgScaled = cv2.resize(img, (300, 300))
imgScaledHSV = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2HSV)

# hsv bounds for color
lower_array = colorFunc.lowerGreen_array
upper_array = colorFunc.upperGreen_array

# extract color from imgScaled
maskTotal = colorFunc.extractMask(imgScaledHSV, lower_array, upper_array)
result = cv2.bitwise_and(imgScaled, imgScaled, mask = maskTotal)
cv2.imwrite('/Users/mightymanh/Desktop/mask.jpg', maskTotal)

# show images
cv2.imshow('Scaled', imgScaled)
cv2.imshow('mask', maskTotal)
# cv2.imshow('result', result)
cv2.waitKey(0)

