'''
    Given a target image that has size around 125 * 125, read letter on it
'''

import os
import cv2
import easyocr
import textDetectionHelper as textDetect

# init hyper variables
stdSize = 125
stdScaledWidth = 125
stdCropSize = 50
step = 10

# init images
reader = easyocr.Reader(['en'])
folderPath = '/Users/mightymanh/Desktop' # put the repo path of image
imgName_list = ['images (1).png'] # put the name of img here

for imgName in imgName_list:
    print(f"------------------------------------\n{imgName}")

    # read img
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # read letter
    textDetect.deepReadImgDetectLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step)

