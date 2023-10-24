import time
import os
from shutil import rmtree

from PIL import Image
from shapely import affinity

import vars
from target import *
from snapshot import *

def main(folder = "", numImg = -1):
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

    # get input for numTargets per snapshot
    numSnapshots = len(os.listdir(vars.noTargetDir))
    if numImg == -1: # default case
        numTargets = int(input("\nThere are in total of 30 snapshots\nHow many target images do you want to generate for each snapshot? \n>> "))
        numTargets = 1 if numTargets == "" else int(numTargets)
    elif numImg <= numSnapshots:
        numTargets = 1
    else:
        numTargets = int(numImg / numSnapshots)

    # get input for folder to write images and labels
    if folder == "":
        folder = vars.targetDir
    
    # get input for type of shape
    shape, rotateTarget, shapeColor, letter, letterColor = targetInputParameters()
    print(numTargets, shape, rotateTarget, shapeColor, letter, letterColor)

    print(f"\nGenerating {numTargets * numSnapshots} target images...\n")

    # generate target images
    start_time = time.time()
    generateTargetImages(folder, numTargets, shape, rotateTarget, shapeColor, letter, letterColor)
    print(f"\ntime: {time.time() - start_time:.2f} seconds\n")
    print(f"The generated images is generated in directory {folder}\n")

# Parameters to create a target: shape, letter, shape color, letter color, rotation
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

    return shape, rotateTarget, shapeColor, letter, letterColor

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
def generateTargetImages(folder, num, shape, rotateTarget, shapeColor, letter, letterColor):
    # check if target directory exists
    if os.path.exists(folder):
        rmtree(folder)
    os.makedirs(folder)

    # remove target-info.csv if it exists
    targetInfoPath = os.path.join(folder, "target_info.csv")
    if os.path.exists(targetInfoPath):
        os.remove(targetInfoPath)
    with open(targetInfoPath, "w") as info:
        info.write("filename,shape,shapeColor,letter,letterColor\n")

    # create directory images
    imageDir = os.path.join(folder, "images")
    if os.path.exists(imageDir):             # if dir exists then delete everything inside
        rmtree(imageDir)
    os.makedirs(imageDir)

    # create directory labels
    labelDir = os.path.join(folder, "labels")
    if os.path.exists(labelDir):             # if dir exists then delete everything inside
        rmtree(labelDir)
    os.makedirs(labelDir)

    # create <num> simulated images for each empty image
    for filename in os.listdir(vars.noTargetDir):
        print(f"Simulating targets for {filename}")
        with Image.open(os.path.join(vars.noTargetDir, filename)) as emptyImage:
            emptyImage = emptyImage.convert("RGBA")
            for i in range(num):
                targetImage = emptyImage.copy() # fix the error where there it accidentally place too many target in an image
                targetFilename = filename[:-4] + f"_tar_{i:03}"

                t1 = placeTarget(targetImage, targetFilename, labelDir, shape, rotateTarget, shapeColor, letter, letterColor)
                t2 = placeTarget(targetImage, targetFilename, labelDir, shape, rotateTarget, shapeColor, letter, letterColor, t1)

                # save image
                targetImage = targetImage.convert("RGB")
                targetImage.save(os.path.join(imageDir, targetFilename + ".jpg"))


# create and place a target on the empty image
def placeTarget(image, filename, labelDir, shape, rotateTarget, shapeColor, letter, letterColor, t1=None):
    # create the target and choose a random location
    targetImage, targetPolygon, targetSeed = createTarget(shape, rotateTarget, shapeColor, letter, letterColor)
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
    yoloString= writeYolo(targetPolygon)
    yoloPath = os.path.join(labelDir, filename + ".txt")
    mode = "a" if os.path.exists(yoloPath) else "w"
    with open(yoloPath, mode) as yoloFile:
        yoloFile.write(yoloString + "\n")

    # place target on image
    xMin, yMin, xMax, yMax = [int(b) for b in targetPolygon.bounds]
    image.alpha_composite(targetImage, dest=(xMin, yMin))

    # # TEST : will be removed later
    # shape = [(xMin, yMin), (xMax, yMax)]
    # image1 = ImageDraw.Draw(image)
    # image1.rectangle(shape, fill=None, outline='red')

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
        center[0] / vars.imageSizePxYolo[0],
        center[1] / vars.imageSizePxYolo[1],
        width / vars.imageSizePxYolo[0],
        height / vars.imageSizePxYolo[1]
    ]  # divide by image dimensions to scale to 1

    yoloString = "0 " + " ".join([f"{y:.8f}" for y in yolo])
    # print(f"  yolo: \"{yoloString}\"")

    return yoloString


if __name__ == "__main__":
    main()
