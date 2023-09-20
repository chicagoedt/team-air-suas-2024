'''
    redefine findShape() in y_targetLocateHelper
'''

import cv2
import numpy as np
import copy

# TESTING params
DEBUG = False
SHOW_IMG = False


# detect shapes that is valid (valid size and valid area)
def findShapeInMask(mask, maskName, targetMinSize, targetMaxSize, minRatioBtwAreaContourAndAreaRect, minRatioBtwNumPixelInsideContourAndAreaContour):
    
    if SHOW_IMG:
        copyMask = copy.deepcopy(mask)                          # FOR TESTING
        copyMask = cv2.cvtColor(copyMask, cv2.COLOR_GRAY2BGR)   # FOR TESTING

    # # binarize mask so that black pixel is 255 and white pixel is 0
    # _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # get list of contours
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # process each contour and grab contour that satisfy with size range and minimum area ratio
    possibleTarget_list = []
    for contour in contours:

        # min bounding box of Target
        rect = cv2.minAreaRect(contour)
        width, height = rect[1]
        width = int(width)
        height = int(height)

        # filter contours with valid size
        if targetMinSize <= width and width <= targetMaxSize and targetMinSize <= height and height <= targetMaxSize:
            M = cv2.moments(contour)

            # skip if the area is not valid
            areaContour = M['m00']
            ratioBtwAreaContourAndAreaRect = round(areaContour / (width * height), 3)
            if DEBUG: print('Area of contour: {}, area of rectangle: {} -> ratio: {}'.format(areaContour, width * height, ratioBtwAreaContourAndAreaRect))
            if ratioBtwAreaContourAndAreaRect < minRatioBtwAreaContourAndAreaRect:
                if DEBUG: print('---------------------------')
                continue

            # skip if the number of white pixel inside contour is not valid
            x1, y1, width1, height1 = cv2.boundingRect(contour) # width1, height1 is different to width, height
            numPixelInsideContour = 0
            arrayPixelInsideContour = []  # for TESTING
            for x in range(int(x1), int(x1 + width1)):
                for y in range(int(y1), int(y1 + height1)):
                    if cv2.pointPolygonTest(contour, (x, y), False) == 1:     # count number of white pixel inside contour
                        if mask[y][x] >= 127:
                            arrayPixelInsideContour.append((x, y)) # for TESTING
                            numPixelInsideContour += 1
            ratioBtwNumPixelInsideContourAndAreaContour = round(numPixelInsideContour / areaContour, 3)
            if DEBUG: print('Number of white pixels inside contour: {}, area: {} -> ratio: {}'.format(numPixelInsideContour, areaContour, ratioBtwNumPixelInsideContourAndAreaContour))
            if ratioBtwNumPixelInsideContourAndAreaContour < minRatioBtwNumPixelInsideContourAndAreaContour:
                if DEBUG: print('---------------------------')
                continue
            
            # get centroid of contour
            cx = int(M['m10']/M['m00']) 
            cy = int(M['m01']/M['m00'])
            centroid = (cx, cy)

            # get average size
            averageSize = int((width1 + height1) / 2)

            # add to the list
            if DEBUG:
                print('Info about contour: width: {}, height: {}, area: {}, centroid: {}, average size: {}'.format(width, height, areaContour, centroid, averageSize))
            possibleTarget_list.append([maskName, centroid, averageSize])
                                        # color, centroid, target average size

            # SHOW IMG
            
            if SHOW_IMG:
                # fill white pixel inside contour with blue dots
                for point in arrayPixelInsideContour:                                      # for TESTING
                    copyMask[point[1]][point[0]] = [255, 0, 0]                             # for TESTING

                # draw yellow box surrouding the found target
                box = cv2.boxPoints(rect)                                                  # for TESTING
                box = np.intp(box)                                                         # for TESTING
                copyMask = cv2.drawContours(copyMask, [box], 0, (0,255,255), 2)            # for TESTING                                                   # for TESTING
            
                # draw contour
                copyMask = cv2.drawContours(copyMask, [contour], 0, (0, 0, 255), 2)        # for TESTING
    if SHOW_IMG:
        cv2.imshow(maskName, copyMask)                                    # for TESTING
        cv2.waitKey(0)                                                    # for TESTING

    return possibleTarget_list
