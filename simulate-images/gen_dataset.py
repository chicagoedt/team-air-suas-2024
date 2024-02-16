'''
    Generating dataset for YOLO model
    possible shapes: 'triangle', 'pentagon', 'circle', 'semicircle', 'quartercircle', 'rectangle', 'star', 'cross'
'''

import os
from shutil import rmtree
from PIL import Image
import time
import random
from shapely.geometry import box
from shapely import affinity
from PIL import ImageFilter

import newSnapshot
import newVars

from target import createTarget, moveTarget
from gen_practice_images import createStoreFolder, writeYolo, placeTarget
allShapes = ['triangle', 'pentagon', 'circle', 'semicircle', 'quartercircle', 'rectangle', 'star', 'cross']

# set input for dataset that you want to generate
listOfShape = allShapes  # put shape in this list
datasetName = "allShapes"  # put a name to dataset
destFolder = "snapshots"  # put path where you will store the dataset
numImgPerShape = 10   # put number of images you want to generate

# input for GENERATING EMPTY IMAGES: image path, image name, satellitePxPerFt, boundary for snapshot
satelliteImgPackList = [("reference_images/MillerGreenField-330px30ft.jpg", "MillerGreen", 330/30, (0, 0, 3840, 2160)),
                        ("reference_images/runway-4150px360ft.png", "Runway", 4150/360, (400, 400, 4550, 1250)),
                        ("reference_images/YellowField-MillerMeadow-81px10ft.png", "MillerYellow", 81/10, (0, 0, 1261, 662))]
generatedImageSize = (640, 640)
numImgsPerSatelliteImg = 10

# generate the training datasets
def genDataSet():
    scriptDir = os.path.dirname(__file__)
    os.chdir(scriptDir)

    datasetPath = os.path.join("./", destFolder, datasetName)
    trainPath = os.path.join(datasetPath, "train")
    validPath = os.path.join(datasetPath, "valid")
    testPath = os.path.join(datasetPath, "test")
    numTrainImg = round(numImgPerShape * 8.5 / 10) # 85%
    numValidImg = round(numImgPerShape * 1 / 10) # 10%
    numTestImg = round(numImgPerShape * 0.5 / 10)  # 5%

    # create a folder datasetName inside destFolder
    if os.path.exists(datasetPath):
        rmtree(datasetPath)
    os.makedirs(datasetPath)

    # create three folders test, train, valid inside folder datasetName
    createStoreFolder(trainPath)
    createStoreFolder(validPath)
    createStoreFolder(testPath)

    # create data.yaml
    datasetAbsolutePath = os.path.join(scriptDir, destFolder, datasetName)
    genDataYaml(listOfShape, datasetAbsolutePath)

    # for each folder train, valid, test -> gen_train_images.py with percentage of 70, 20, 10
    start_time = time.time()

    # generate new empty images in vars.noTargetDir                              
    if os.path.exists(newVars.noTargetDir):
        rmtree(newVars.noTargetDir)
    os.makedirs(newVars.noTargetDir)               
    generateEmptyImagesPool(satelliteImgPackList, generatedImageSize, numImgsPerSatelliteImg)
  
    classNumber = 0
    for shape in listOfShape:
        # gen images for train, valid, test
        genImages(trainPath, numTrainImg, shape, classNumber)
        genImages(validPath, numValidImg, shape, classNumber)
        genImages(testPath, numTestImg, shape, classNumber)
        classNumber += 1 # increment for next class

    print(f"time: {time.time() - start_time:.2f} seconds\n")
    print(f"The generated images is generated in directory {datasetPath}\n")

# generate a pool of background images
def generateEmptyImagesPool(satelliteImgPackList, size, numImgsPerSatelliteImg):
    
    start_time = time.time()
    for satelliteImgPack in satelliteImgPackList:
        # configuration

        satelliteImg = Image.open(satelliteImgPack[0])
        satelliteImgName = satelliteImgPack[1]
        satellitePxPerFt = satelliteImgPack[2]
        boundaryBox = satelliteImgPack[3]
        newSnapshot.generateEmptyImages(satelliteImg, satelliteImgName, satellitePxPerFt, boundaryBox, size, numImgsPerSatelliteImg)

    print(f"Generate empty images: time: {time.time() - start_time:.2f} seconds\n")

# generate <numImg> training images in folder <path>
def genImages(path, numImg, shape, classNumber):

    print(f"Generating {numImg} target with {shape} images in {path}")

    # path
    imagesPath = os.path.join(path, "images/")
    labelsPath = os.path.join(path, "labels/")

    # list of snapshots for target generating
    listOfSnapshots = os.listdir(newVars.noTargetDir)
    numSnapshots = len(listOfSnapshots)

    # for each target, choose a random snapshot, and place a target at random location
    for i in range(numImg):
        filename = listOfSnapshots[random.randint(0, numSnapshots - 1)] # choose random snapshot
        with Image.open(os.path.join(newVars.noTargetDir, filename)) as emptyImage:
            targetImage = emptyImage.convert("RGBA")
            targetFilename = shape + f"_{i:03}"

            # place a target in snapshot
            seed = [shape, "random", "random", "random", True]
            targetPolygon, _ = placeTarget(targetImage, seed)

            # save image in imagesPath
            targetImage = targetImage.convert("RGB")
            xMin, yMin, xMax, yMax = [int(b) for b in targetPolygon.bounds]
            boxCrop = (xMin, yMin, xMax, yMax)
            ic = targetImage.crop(boxCrop)
            ic = ic.filter(ImageFilter.BoxBlur(3))
            targetImage.paste(ic, boxCrop)
            targetImage.save(os.path.join(imagesPath, targetFilename + ".jpg"))

            # save yolo txt in labelsPath
            yoloString = writeYolo(targetPolygon, classNumber, targetImage.size)
            yoloPath = os.path.join(labelsPath, targetFilename + ".txt")
            with open(yoloPath, "w") as yoloFile:
                yoloFile.write(yoloString + "\n")

# generate data.yaml about the dataset
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