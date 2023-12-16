import os
from shutil import rmtree
from PIL import Image
import time
import vars
import random

import gen_train_images as genTrain

# set input for dataset that you want to generate
listOfShape = ['triangle', 'rectangle']
datasetName = "triAndRec"
destFolder = "snapshots"
numImgPerShape = 30

def genDataSet():
    scriptDir = os.path.dirname(__file__)
    os.chdir(scriptDir)

    datasetPath = os.path.join("./", destFolder, datasetName)
    trainPath = os.path.join(datasetPath, "train")
    validPath = os.path.join(datasetPath, "valid")
    testPath = os.path.join(datasetPath, "test")
    numTrainImg = round(numImgPerShape * 7 / 10) # 70%
    numValidImg = round(numImgPerShape * 2 / 10) # 20%
    numTestImg = round(numImgPerShape * 1 / 10)  # 10%

    # create a folder datasetName inside destFolder
    if os.path.exists(datasetPath):
        rmtree(datasetPath)
    os.makedirs(datasetPath)

    # create three folders test, train, valid inside folder datasetName
    os.makedirs(trainPath)
    os.makedirs(validPath)
    os.makedirs(testPath)
    os.makedirs(os.path.join(trainPath, "images"))
    os.makedirs(os.path.join(trainPath, "labels"))
    os.makedirs(os.path.join(validPath, "images"))
    os.makedirs(os.path.join(validPath, "labels"))
    os.makedirs(os.path.join(testPath, "images"))
    os.makedirs(os.path.join(testPath, "labels"))

    # create data.yaml
    datasetAbsolutePath = os.path.join(scriptDir, destFolder, datasetName)
    genDataYaml(listOfShape, datasetAbsolutePath)

    # for each folder train, valid, test -> gen_train_images.py with percentage of 70, 20, 10
    start_time = time.time()
    classNumber = 0
    for shape in listOfShape:
        # generate new empty images in vars.noTargetDir                              
        if os.path.exists(vars.noTargetDir):
            rmtree(vars.noTargetDir)
        os.makedirs(vars.noTargetDir)               
        genTrain.generateEmptyImages(Image.open("reference_images/runway.png"))

        # gen images for train, valid, test
        genImages(trainPath, numTrainImg, shape, classNumber)
        genImages(validPath, numValidImg, shape, classNumber)
        genImages(testPath, numTestImg, shape, classNumber)
        classNumber += 1 # increment for next class

    print(f"time: {time.time() - start_time:.2f} seconds\n")
    print(f"The generated images is generated in directory {datasetPath}\n")

def genImages(path, numImg, shape, classNumber):

    print(f"Generating {numImg} target with {shape} images in {path}")

    # path
    imagesPath = os.path.join(path, "images/")
    labelsPath = os.path.join(path, "labels/")

    # list of snapshots for target generating
    listOfSnapshots = os.listdir(vars.noTargetDir)
    numSnapshots = len(listOfSnapshots)

    # for each target, choose a random snapshot, and place a target at random location
    for i in range(numImg):
        filename = listOfSnapshots[random.randint(0, numSnapshots - 1)] # choose random snapshot
        with Image.open(os.path.join(vars.noTargetDir, filename)) as emptyImage:
            targetImage = emptyImage.convert("RGBA")
            targetFilename = shape + f"_{i:03}"

            # place a target in snapshot
            targetPolygon = placeTarget(targetImage, shape)

            # save image in imagesPath
            targetImage = targetImage.convert("RGB")
            targetImage.save(os.path.join(imagesPath, targetFilename + ".jpg"))

            # save yolo txt in labelsPath
            yoloString = writeYolo(targetPolygon, classNumber)
            yoloPath = os.path.join(labelsPath, targetFilename + ".txt")
            with open(yoloPath, "w") as yoloFile:
                yoloFile.write(yoloString + "\n")


# create and place a target on the empty image
def placeTarget(image, shape):
    # create the target and choose a random location
    targetImage, targetPolygon, targetSeed = genTrain.createTarget(shape, True, "random", "random", "random")
    targetPolygon = genTrain.moveTarget(targetPolygon)

    # place target on image
    xMin, yMin, xMax, yMax = [int(b) for b in targetPolygon.bounds]
    image.alpha_composite(targetImage, dest=(xMin, yMin))

    return targetPolygon

# write the yolo file containing the location of the target on the image
def writeYolo(polygon, classNumber):
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

    yoloString = str(classNumber) + " " + " ".join([f"{y:.8f}" for y in yolo])
    # print(f"  yolo: \"{yoloString}\"")

    return yoloString


def genDataYaml(listOfShape, datasetAbsolutePath):
    trainPath = os.path.join(datasetAbsolutePath, "train")
    validPath = os.path.join(datasetAbsolutePath, "valid")
    testPath = os.path.join(datasetAbsolutePath, "test")
    yamlPath = os.path.join(datasetAbsolutePath, "data.yaml")
    with open(yamlPath, "w") as yamlFile:
        yamlFile.write("path: ")
        yamlFile.write(datasetAbsolutePath)
        yamlFile.write("\ntrain: ")
        yamlFile.write(trainPath)
        yamlFile.write("\nval: ")
        yamlFile.write(validPath)
        yamlFile.write("\ntest: ")
        yamlFile.write(testPath)
        yamlFile.write("\n\nnc: ")
        yamlFile.write(str(len(listOfShape)))
        yamlFile.write("\nnames: ")
        yamlFile.write(str(listOfShape))
        

if __name__ == "__main__":
    genDataSet()