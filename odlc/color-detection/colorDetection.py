'''
    given target image, detect shape color and letter color
'''

import cv2
import os
import colorDetectionHelper as colorDetect

# init hyper variables
stdCropColorRatio = 40 / 125

# init images
folder_path = '/Users/mightymanh/Desktop/myCode/temporary_2023/simulate-images/snapshots/target_practice'
imgName_list = ['img_001_tar_001.jpg']

for imgName in imgName_list:
    print(f"--------------------------\n{imgName}")
    imgPath = os.path.join(folder_path, imgName)
    img = cv2.imread(imgPath)

    # get shape and letter color
    shapeColor, letterColor = colorDetect.readImgGetShapeAndLetterColor(img, stdCropColorRatio)

