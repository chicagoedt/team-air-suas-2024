'''
    A more dynamic version of snapshot.py
    The functions here take picture from many satellite images and are less dependent on the vars
'''

from shapely.geometry import box
from shapely import affinity
from numpy import ravel
from PIL.ImageTransform import QuadTransform
from PIL import Image

from shutil import rmtree
import time, random, os

import newVars

# generate empty images with configurations
def generateEmptyImages(satelliteImg, satelliteImgName, satellitePxPerFt, boundaryBox, size, numImgs):
    
    print("Generating empty image:", satelliteImgName)

    # determine the size of snapshot
    (snapshotWidth, snapshotHeight) = [int(dim * satellitePxPerFt) for dim in newVars.imageSizeFt]

    # create snapshot polygon and shift it to the upper right corner of the air drop boundary
    snapshot = box(0, 0, snapshotWidth, snapshotHeight)
    snapshot = affinity.translate(
        snapshot,
        xoff=boundaryBox[0],
        yoff=boundaryBox[1]
    )

    # create <numImgs> number of empty images
    for i in range(numImgs):
        randomSnapshot = getNewSnapshot(snapshot, boundaryBox, (snapshotWidth, snapshotHeight))

        # save snapshot image
        droneImage = takePicture(satelliteImg, randomSnapshot, size)
        droneImage = droneImage.convert("RGB")
        droneImage.save(os.path.join(newVars.noTargetDir, f"{satelliteImgName}_{i:03}.jpg"))

# given the satellite image, create a new image with the boundaries of the snapshot
def takePicture(satelliteImg, snapshot, size):
    snapshotCorners = ravel((snapshot.exterior.coords[3] + snapshot.exterior.coords[2] +
                            snapshot.exterior.coords[1] + snapshot.exterior.coords[0]))
    img = satelliteImg.transform(size, QuadTransform(snapshotCorners))
    return img

# get a random snapshot based on original snapshot (img)
def getNewSnapshot(snapshot, boundaryBox, snapshotSize):
    # choose a random location in the image
    xOffset = random.randint(boundaryBox[0], boundaryBox[2] - snapshotSize[0])
    yOffset = random.randint(boundaryBox[1], boundaryBox[3] - snapshotSize[1])

    # get new snapshot by shifting original snapshot by offsets x and y
    newSnapshot = affinity.translate(snapshot, xoff=xOffset, yoff=yOffset)
    return newSnapshot

if __name__ == "__main__":
    if os.path.exists(newVars.noTargetDir):
        rmtree(newVars.noTargetDir)
    os.makedirs(newVars.noTargetDir) 

    # configuration
    satelliteImg = Image.open("reference_images/MillerGreenField-330px30ft.jpg")
    satelliteImgName = "MillerGreen"
    satellitePxPerFt = 330 / 30
    boundaryBox = [0, 0, 3840, 2160]
    size = (4056, 3040)
    numImgs = 20

    # generate empty images
    generateEmptyImages(satelliteImg, satelliteImgName, satellitePxPerFt, boundaryBox, size, numImgs)      