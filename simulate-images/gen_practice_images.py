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
        generateEmptyImages(runway, vars.imageSizePx)

    # get input for numTargets per snapshot
    numTargets = int(input("\nHow many target images do you want to generate? \n>> "))
    
    # get input for type of target
    seed = targetInputParameters() # shape, shape color, letter, letter color, rotation
    print(f"\nnumTargets: {numTargets}, shape: {seed[0]}, shape color: {seed[1]}, letter: {seed[2]}, letter color: {seed[3]}, rotation: {seed[4]}")
    
    # create folder structure
    createStoreFolder(vars.targetDir)

    # generate target images
    start_time = time.time()
    print("Start generating ...")
    generateTargetImages(vars.targetDir, numTargets, seed)
    print(f"\ntime: {time.time() - start_time:.2f} seconds\n")
    print(f"The generated images is generated in directory {vars.targetDir}\n")

# Parameters to create a target: shape, shape color, letter, letter color, rotation
def targetInputParameters(): 
    # user inputs
    shape = input("What shape? Possible shapes: " + str(shapes) + " \n(press enter for random) >> ")
    shape = "random" if shape == "" else shape

    rotateTarget = True if input("Rotate target? \n(press enter for yes) >> ") == "" else False

    shapeColor = input("What shape color? Possible colors: " + str(list(colors)) + " \n(press enter for random) >> ")
    shapeColor = "random" if shapeColor == "" else shapeColor

    letter = input("What letter? \n(press enter for random) >> ")
    letter = "random" if letter == "" else letter

    letterColor = input("What letter color? \n(press enter for random) >> ")
    letterColor = "random" if letterColor == "" else letterColor

    return shape, shapeColor, letter, letterColor, rotateTarget # seed of a target

# create the runway images that the targets will be placed on
def generateEmptyImages(runway, size):
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
        droneImage = takePicture(runway, snapshot, size)
        droneImage = droneImage.convert("RGB")
        droneImage.save(os.path.join(vars.noTargetDir, f"img_{count:03}.jpg"))
        count += 1

        # move down and to the right as necessary
        snapshot = shiftSnapshot(snapshot)

    print(f"time: {time.time() - start_time:.2f} seconds")

# create a folder hierachy for storing generated images and txts
def createStoreFolder(folder):
    # check if target directory exists
    if os.path.exists(folder):
        rmtree(folder)
    os.makedirs(folder)

    # create directory images
    imageDir = os.path.join(folder, "images")
    os.makedirs(imageDir)

    # create directory labels
    labelDir = os.path.join(folder, "labels")
    os.makedirs(labelDir)

# create runway images with targets on them and create yolo txt files associate with them
def generateTargetImages(folder, num, seed):

    imageDir = os.path.join(folder, "images")
    labelDir = os.path.join(folder, "labels")

    # remove target-info.csv if it exists
    targetInfoPath = os.path.join(folder, "target_info.csv")
    if os.path.exists(targetInfoPath):
        os.remove(targetInfoPath)
    with open(targetInfoPath, "w") as info:
        info.write("filename,shape,shapeColor,letter,letterColor\n")

    # list of snapshots for target generating
    listOfSnapshots = os.listdir(vars.noTargetDir)
    numSnapshots = len(listOfSnapshots)

    # for each target, choose a random snapshot, and place a target at random location
    for i in range(num):
        filename = listOfSnapshots[random.randint(0, numSnapshots - 1)] # choose random snapshot
        with Image.open(os.path.join(vars.noTargetDir, filename)) as emptyImage:
            targetImage = emptyImage.convert("RGBA")
            targetFilename =  f"img_{i:03}"

            # place a target in snapshot
            targetPolygon, targetSeed = placeTarget(targetImage, seed)

            # save seed to csv
            with open(targetInfoPath, "a") as info:
                info.write(f"{targetFilename},{targetSeed['shape']},{targetSeed['shapeColor']},{targetSeed['letter']},{targetSeed['letterColor']}\n")

            # save image in imagesPath
            targetImage = targetImage.convert("RGB")
            targetImage.save(os.path.join(imageDir, targetFilename + ".jpg"))

            # save yolo txt in labelsPath
            yoloString = writeYolo(targetPolygon, YOLOs[targetSeed["shape"]], vars.imageSizePx)
            yoloPath = os.path.join(labelDir, targetFilename + ".txt")
            with open(yoloPath, "w") as yoloFile:
                yoloFile.write(yoloString + "\n")

# create and place a target on the empty image
def placeTarget(image, seed):
    # create the target and choose a random location
    targetImage, targetPolygon, targetSeed = createTarget(seed)
    targetPolygon = moveTarget(targetPolygon, image.size)

    # place target on image
    xMin, yMin, xMax, yMax = [int(b) for b in targetPolygon.bounds]
    image.alpha_composite(targetImage, dest=(xMin, yMin))

    return targetPolygon, targetSeed

# write the yolo file containing the location of the target on the image
def writeYolo(polygon, classNumber, imgSize):
    xMin, yMin, xMax, yMax = [int(b) for b in polygon.bounds]
    width = xMax - xMin
    height = yMax - yMin

    # find centerpoint of target
    center = [int(c) for c in polygon.centroid.coords[0]]
    # print("  center:", center)

    # write yolo file in this format:
    #   0 <bbox center x> <bbox center y> <bbox width> <bbox height>
    yolo = [
        center[0] / imgSize[0],
        center[1] / imgSize[1],
        width / imgSize[0],
        height / imgSize[1]
    ]  # divide by image dimensions to scale to 1

    yoloString = str(classNumber) + " " + " ".join([f"{y:.8f}" for y in yolo]) # set to default 0
    # print(f"  yolo: \"{yoloString}\"")

    return yoloString


if __name__ == "__main__":
    main()
