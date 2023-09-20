'''
    Tools for preprocess image
'''

import cv2
import os

# scale image from W * L -> newWidth * (L * newWidth / W)
# if pass newWidth = 0 then we do not scale
def scaleImg(img, newWidth): 
    if newWidth == 0:
        return img
    size = img.shape # a tuple (side1, side2, rgb)
    width = min(size[0], size[1]) # find which side is width (the smaller side)
    new_size = (int(size[1] * newWidth / width), int(size[0] * newWidth / width)) 
    scaled_img = cv2.resize(img, new_size) # scale to new_size
    return scaled_img 

# crop image to rectange whose center = centerCoords and has dimension = width * height
def cropImage(img, centerCoords, width, height):
    maxWidth = img.shape[1]
    maxHeight = img.shape[0]
    startRow = centerCoords[1] - int(height / 2)
    endRow = centerCoords[1] + int(height / 2)
    startCol = centerCoords[0] - int(width / 2)
    endCol = centerCoords[0] + int(width / 2)
    
    # edge case
    if startRow < 0:
        startRow = 0
    if endRow >= maxHeight:
        endRow = maxHeight
    if startCol < 0:
        startCol = 0
    if endCol >= maxWidth:
        endCol = maxWidth
    cropped = img[startRow:endRow, startCol:endCol]
    return cropped

# function that changes brightness and contrast level of an img
# borrow from Stack overflow, similar to what GIMP does
# input value for brightness and contrast should be in range -127 to 127, including both ends
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf
