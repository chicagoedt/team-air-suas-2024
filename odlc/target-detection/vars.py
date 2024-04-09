from math import sqrt, atan, tan

from shapely.geometry.polygon import Polygon
from shapely.geometry import box
import random

# directories
noTargetDir = "snapshots/no_target/"
imageDir = "snapshots/target/images"
labelDir = "snapshots/target/labels"
targetDir = "snapshots/target/"
targetPracticeDir = "snapshots/target_practice/"
resourceDir = "target_resources/"
targetInfoPath = "snapshots/target/target_info.csv"
targetPracticeInfoPath = "snapshots/target_practice_info.csv"

# constants
sensorSize = 7.9  # mm
focalLength = 16  # mm
droneHeight = 100 # ft
imageSizePx = (4056, 3040)  # px
targetSizeFt = (8.5 / 12, 11 / 12)  # ft (8.5x11" page)
satelliteSizePx = (4950, 1650) # px
runwayPxPerFt = 4150 / 360 # px/ft
# useful vars for YOLO customTrain
imageSizePxYolo = (640, 640)
# constant shapes
airDropBoundary = box(400, 400, 4550, 1250)

# calculated values
imageDiagPx = sqrt(imageSizePx[0] ** 2 + imageSizePx[1] ** 2)  # px
viewAngle = 2 * atan(sensorSize / 2 / focalLength)  # rad
imageDiagFt = 2 * droneHeight * tan(viewAngle / 2)  # ft

# final values
pxPerFt = imageDiagPx / imageDiagFt  # px/ft
imageSizeFt = [l / pxPerFt for l in imageSizePx]  # ft
scaleFactor = pxPerFt / runwayPxPerFt  # no unit # scaleFactor is the ratio of satellite img (px) -> 4K by 3K snapshot img (px)
(snapshotWidth, snapshotHeight) = [int(dim * runwayPxPerFt) for dim in imageSizeFt]  # px
targetSize = [int(f * pxPerFt) for f in targetSizeFt]  # px

# function to change global values that depend on drone height
def exportValuesDroneHeight():
    global droneHeight, imageDiagFt, pxPerFt, imageSizeFt, scaleFactor, snapshotWidth, snapshotHeight, targetSize
    droneHeight = random.randint(25, 110)
    imageDiagFt = 2 * droneHeight * tan(viewAngle / 2)
    pxPerFt = imageDiagPx / imageDiagFt  # px/ft
    imageSizeFt = [l / pxPerFt for l in imageSizePx]  # ft
    scaleFactor = pxPerFt / runwayPxPerFt  # no unit # scaleFactor is the ratio of satellite img (px) -> 4K by 3K snapshot img (px)
    (snapshotWidth, snapshotHeight) = [int(dim * runwayPxPerFt) for dim in imageSizeFt]  # px
    targetSize = [int(f * pxPerFt) for f in targetSizeFt]  # px

def exportValuesDroneHeight(dH):
    global imageDiagFt, pxPerFt, imageSizeFt, scaleFactor, snapshotWidth, snapshotHeight, targetSize
    imageDiagFt = 2 * dH * tan(viewAngle / 2)
    pxPerFt = imageDiagPx / imageDiagFt  # px/ft
    imageSizeFt = [l / pxPerFt for l in imageSizePx]  # ft
    scaleFactor = pxPerFt / runwayPxPerFt  # no unit # scaleFactor is the ratio of satellite img (px) -> 4K by 3K snapshot img (px)
    (snapshotWidth, snapshotHeight) = [int(dim * runwayPxPerFt) for dim in imageSizeFt]  # px
    targetSize = [int(f * pxPerFt) for f in targetSizeFt]  # px

if __name__ == "__main__":
    print("targetSize:", targetSize)
    print("pxPerFt:", pxPerFt)