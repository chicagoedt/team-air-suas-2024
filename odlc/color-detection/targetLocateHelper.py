'''
    Helper functions for y_targetLocate.py
'''

import cv2
import numpy as np
import os
import tool_colorFunc as colorFunc              # color
import tool_adaptToRealLife as adapt            # real image: light level
import tool_imgPreprocessing as prepr           # preprocessing img
import tool_nameFormatHelper as nameHelper        # deal with file name
import findShapeInMask as findTar

DEBUG = False
SHOW_IMG = False

# preprocessing img before locating targets
def imgPreprocessing(img):
    lightLevel = adapt.measureBackgroundLightLevel(img)
    brightnessChange, contrastChange = adapt.getBrightnessContrastChange(lightLevel)
    if DEBUG: print('brightnessChange: {}, contrastChange: {}'.format(brightnessChange, contrastChange))
    img = prepr.apply_brightness_contrast(img, brightnessChange, contrastChange)
    return img

# return a list of color-filtered masks
def collectingMasks(img):
    if DEBUG: print('>> Begin collecting masks')
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # collecting mask
    maskList = []
    for color in colorFunc.colorDict.keys():
        lowerArray, upperArray = colorFunc.colorDict[color]
        mask = colorFunc.extractMask(imgHSV, lowerArray, upperArray)
        maskList.append((color, mask))
    if DEBUG: print('>> Finish collecting masks')
    return maskList

# write masks to a folder
def writeMaskToMaskFolder(maskList, destFolder):
    if DEBUG: print('>> Begin writing mask')
    imgName_list = []
    for mask in maskList:
        maskName = mask[0] + '.jpg'
        imgName_list.append(maskName)
        if DEBUG: print('Writing mask image {}'.format(maskName))
        destPath = os.path.join(destFolder, maskName)
        cv2.imwrite(destPath, mask[1])
    
    if DEBUG: print('>> Finish writing mask:', imgName_list)
    return imgName_list

# main function that locates targets and also determine its shape color, continue after collecting mask
def targetLocation(img, stdTargetMinSize, stdTargetMaxSize, stdMinRatioBtwAreaContourAndAreaRect, stdMinRatioBtwNumPixelInsideContourAndAreaContour):

    # collect mask
    mask_list = collectingMasks(img)

    # target localization
    TargetFound_list = []
    if DEBUG: print('>> Begin targetLocation:')
    for mask in mask_list:
        # init imgMask
        color = mask[0]
        imgMask = mask[1]
        if DEBUG: print(color)

        # detect possible targets
        TargetFound_list.extend(findTar.findShapeInMask(imgMask, color, stdTargetMinSize, stdTargetMaxSize, stdMinRatioBtwAreaContourAndAreaRect, stdMinRatioBtwNumPixelInsideContourAndAreaContour))
        if DEBUG: print('------------------------------------------------')
    
    if DEBUG: print('>> Finish targetLocation!')
    return TargetFound_list
            # color, centroid, averageSize

# cropping targets from input img
# after locating the possibile targets, crop them and save them to dest folder
def cropFoundTargets(img, imgName, TargetFound_list, destFolder, enableClearOldFiles, ImgTargetRatio):
    if DEBUG: print('>> Begin cropFoundTargets. Clear old files =', enableClearOldFiles)
    if enableClearOldFiles:
        # clear destFolder first
        oldFiles = os.listdir(destFolder)
        if len(oldFiles) != 0:
            for file in oldFiles:
                os.remove(os.path.join(destFolder, file))

    crop_list = []
    # for each found target, crop it
    for targetFound in TargetFound_list:
        
        # get info of target
        centerCoords = (int(targetFound[1][0]), int(targetFound[1][1]))
        originalImgName = nameHelper.cutExtension(imgName)
        shapeColor = targetFound[0]
        targetSize = targetFound[2]
    
        # crop target and add crop to crop_list
        cropSize = int(targetSize * ImgTargetRatio)
        if DEBUG: print('targetSize: {}, ImgTargetRatio: {} -> cropSize: {}'.format(targetFound[2], ImgTargetRatio, cropSize))
        crop = prepr.cropImage(img, centerCoords, cropSize, cropSize)
        crop_list.append((originalImgName, centerCoords, shapeColor, crop))

        # FOR EXPORTING CROP TO IMAGES
        # get name for crop file, get path for crop file
        cropName = originalImgName + '_' + str(centerCoords[0]) + '-' + str(centerCoords[1]) + '_' + shapeColor + '.jpg'
                   # <originalImgName>_<centerCoords>_<targetShapeColor>.jpg
        print('creating file {}\n-----------------------------------'.format(cropName))
        
        # write crop to destFolder
        cropPath = os.path.join(destFolder, cropName)
        cv2.imwrite(cropPath, crop)
    if DEBUG: print('>> Finish cropFoundTargets!')

    return crop_list
