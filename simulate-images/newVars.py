from math import sqrt, atan, tan

# directories
noTargetDir = "snapshots/no_target/"
imageDir = "snapshots/target/images"
labelDir = "snapshots/target/labels"
targetDir = "snapshots/target/"
targetPracticeDir = "snapshots/target_practice/"
resourceDir = "target_resources/"
targetInfoPath = "snapshots/target/target_info.csv"
targetPracticeInfoPath = "snapshots/target_practice_info.csv"

# constants for Camera & Sensor
sensorSize = 7.9  # mm
focalLength = 16  # mm
droneHeight = 100  # ft

# constant for expected image's size and the target's size
imageSizePx = (4056, 3040)  # px
targetSizeFt = (8.5 / 12, 11 / 12)  # ft (8.5x11" page)

# calculated values
imageDiagPx = sqrt(imageSizePx[0] ** 2 + imageSizePx[1] ** 2)  # px
viewAngle = 2 * atan(sensorSize / 2 / focalLength)  # rad
imageDiagFt = 2 * droneHeight * tan(viewAngle / 2)  # ft

# final values
pxPerFt = imageDiagPx / imageDiagFt  # px/ft
imageSizeFt = [l / pxPerFt for l in imageSizePx]  # ft
targetSize = [int(f * pxPerFt) for f in targetSizeFt]  # px