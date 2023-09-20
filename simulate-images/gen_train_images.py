import time
import os
from shutil import rmtree

from PIL import Image
from shapely import affinity

import vars
from target import *
from snapshot import *


def main():
    os.chdir(os.path.dirname(__file__))

    # open runway image
    runway = Image.open("reference_images/runway.png")

    # check if empty images have already been generated
    generateNew = True
    if os.path.exists(vars.noTargetDir):
        generateNew = input(
            "\nLooks like you have already generated empty runway images. Would you like to generate new ones?\n  (y/N) >> ")
        generateNew = True if generateNew == "y" else False

    if generateNew:
        if os.path.exists(vars.noTargetDir):
            rmtree(vars.noTargetDir)
        os.makedirs(vars.noTargetDir)
        generateEmptyImages(runway)

    numSnapshots = len(os.listdir(vars.noTargetDir))

    numTargets = int(
        input("\nHow many target images do you want to generate for each snapshot? >> "))
    print(f"\nGenerating {numTargets * numSnapshots} target images...\n")

    start_time = time.time()
    generateTargetImages(numTargets)
    print(f"\ntime: {time.time() - start_time:.2f} seconds\n")


# create the runway images that the targets will be placed on
def generateEmptyImages(runway):
    print("\nGenerating empty images...")
    start_time = time.time()

    # create snapshot polygon and shift it to the upper right corner of the air drop boundary
    snapshot = box(0, 0, vars.snapshotWidth, vars.snapshotHeight)
    snapshot = affinity.translate(
        snapshot,
        xoff=vars.airDropBoundary.bounds[0],
        yoff=vars.airDropBoundary.bounds[1]
    )

    # create images of runway
    count = 0
    while snapshot.intersects(vars.airDropBoundary):
        # save snapshot image
        droneImage = takePicture(runway, snapshot)
        droneImage = droneImage.convert("RGB")
        droneImage.save(os.path.join(vars.noTargetDir, f"img_{count:03}.jpg"))
        count += 1

        # move down and to the right as necessary
        snapshot = shiftSnapshot(snapshot)

    print(f"time: {time.time() - start_time:.2f} seconds")


# create runway images with targets on them
def generateTargetImages(num):
    # check if target directory exists
    if os.path.exists(vars.targetDir):
        rmtree(vars.targetDir)
    os.makedirs(vars.targetDir)

    # remove target-info.csv if it exists
    if os.path.exists(vars.targetInfoPath):
        os.remove(vars.targetInfoPath)
    with open(vars.targetInfoPath, "w") as info:
        info.write("filename,shape,shapeColor,letter,letterColor\n")

    # create <num> simulated images for each empty image
    for filename in os.listdir(vars.noTargetDir):
        print(f"Simulating targets for {filename}")
        with Image.open(os.path.join(vars.noTargetDir, filename)) as emptyImage:
            emptyImage = emptyImage.convert("RGBA")
            for i in range(num):
                targetImage = emptyImage
                targetFilename = filename[:-4] + f"_tar_{i:03}"

                t1 = placeTarget(targetImage, targetFilename)
                t2 = placeTarget(targetImage, targetFilename, t1)

                # save image
                targetImage = targetImage.convert("RGB")
                targetImage.save(os.path.join(vars.targetDir, targetFilename + ".jpg"))


# create and place a target on the empty image
def placeTarget(image, filename, t1=None):
    # create the target and choose a random location
    targetImage, targetPolygon, targetSeed = createTarget()
    targetPolygon = moveTarget(targetPolygon, t1)

    # DEBUG: check if a second target was placed
    if t1 is not None:
        if targetPolygon is None:
            return None
        else:
            print(f"  {filename} has 2 targets")

    # save seed to csv
    with open(vars.targetInfoPath, "a") as info:
        seed = [i for i in targetSeed.values()][:4]
        info.write(f"{filename},{','.join(seed)}\n")

    # create/write to yolo file for target
    yoloString = writeYolo(targetPolygon)
    yoloPath = os.path.join(vars.targetDir, filename + ".yolo")
    mode = "a" if os.path.exists(yoloPath) else "w"
    with open(yoloPath, mode) as yoloFile:
        yoloFile.write(yoloString + "\n")

    # place target on image
    xMin, yMin, xMax, yMax = [int(b) for b in targetPolygon.bounds]
    image.alpha_composite(targetImage, dest=(xMin, yMin))

    return targetPolygon


# write the yolo file containing the location of the target on the image
def writeYolo(polygon):
    xMin, yMin, xMax, yMax = [int(b) for b in polygon.bounds]
    width = xMax - xMin
    height = yMax - yMin

    # find centerpoint of target
    center = [int(c) for c in polygon.centroid.coords[0]]
    # print("  center:", center)

    # write yolo file in this format:
    #   0 <bbox center x> <bbox center y> <bbox width> <bbox height>
    yolo = [
        center[0] / vars.imageSizePx[0],
        center[1] / vars.imageSizePx[1],
        width / vars.imageSizePx[0],
        height / vars.imageSizePx[1]
    ]  # divide by image dimensions to scale to 1

    yoloString = "0 " + " ".join([f"{y:.8f}" for y in yolo])
    # print(f"  yolo: \"{yoloString}\"")

    return yoloString


if __name__ == "__main__":
    main()
