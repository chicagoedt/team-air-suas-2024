import os
from shutil import rmtree
from gen_train_images import main

datasetName = "triangleRotate"
destFolder = "./snapshots"
totalImg = 300 * 180

datasetPath = os.path.join(destFolder, datasetName)
trainPath = os.path.join(datasetPath, "train")
validPath = os.path.join(datasetPath, "valid")
testPath = os.path.join(datasetPath, "test")
numTrainImg = totalImg * 7 / 10 # 70%
numValidImg = totalImg * 2 / 10 # 20%
numTestImg = totalImg * 1 / 10  # 10%

# create a folder datasetName inside destFolder
if os.path.exists(datasetPath):
    rmtree(datasetPath)
os.makedirs(datasetPath)

# create three folders test, train, valid inside datasetName
os.makedirs(trainPath)
os.makedirs(validPath)
os.makedirs(testPath)

# create data.yaml (optional)

# for each folder train, valid, test -> gen_train_images.py with percentage of 70, 20, 10
main(trainPath, numTrainImg)
main(validPath, numValidImg)
main(testPath, numTestImg)