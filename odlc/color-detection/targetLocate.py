'''
    Goal: locate targets on gray background using color (except gray objects)
'''
import os
import cv2
import targetLocateHelper as targetLoc
import tool_imgPreprocessing as prepr

# init hypervariables
stdTargetMinSize = 40
stdTargetMaxSize = 120
stdMinRatioBtwAreaContourAndAreaRect = 1/3
stdMinRatioBtwNumPixelInsideContourAndAreaContour = 0.5
stdImgTargetRatio = 10 / 6 # the ratio the size of crop target image and the size of target

# input images and folder
folderPath = ''
imgName_list = ['img_023_tar_000.jpg']
destFolderForCrop = 'cropImages'

# for each image get centerCoords, Area of target, Shape color, width * height of target
for imgName in imgName_list:
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # preprocessing image
    imgPreprocessed = targetLoc.imgPreprocessing(img)
    # cv2.imshow('imgPreprocessed', imgPreprocessed)   # TESTING
    # cv2.waitKey(0)                                   # TESTING

    # target locating
    TargetFound_list = targetLoc.targetLocation(imgPreprocessed, stdTargetMinSize, stdTargetMaxSize, stdMinRatioBtwAreaContourAndAreaRect, stdMinRatioBtwNumPixelInsideContourAndAreaContour)
    for targetFound in TargetFound_list:
        print(targetFound)
        # color, centerCoords, targetSize

    # cropping targets from input img / imgPreprocessed
    cropList = targetLoc.cropFoundTargets(imgPreprocessed, imgName, TargetFound_list, destFolderForCrop, True, stdImgTargetRatio)



