'''
    given target image, detect shape color and letter color
'''

import cv2
import os
import colorDetectionHelper as colorDetect

# init hyper variables
stdCropColorRatio = 40 / 125

# init images
folder_path = ''
imgName_list = ['img_020_tar_001.jpg']

for imgName in imgName_list:
    print(f"--------------------------\n{imgName}")
    imgPath = os.path.join(folder_path, imgName)
    img = cv2.imread(imgPath)

    # get shape and letter color
    shapeColor, letterColor = colorDetect.readImgGetShapeAndLetterColor(img, stdCropColorRatio)

