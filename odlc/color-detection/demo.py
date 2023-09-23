import cv2

# init img
imgPath = '/Users/aidenlee/Desktop/team air/team-air-suas-2024/odlc/color-detection/img_020_tar_001.jpg'

# read images 
img = cv2. imread(imgPath)

#show img
cv2.imshow('demo', img)
cv2.waitKey(0)

