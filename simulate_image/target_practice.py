import os
from shutil import rmtree

from PIL import Image

import vars
from sim_image import SimImage
from gen_train_images import generateEmptyImages


def main():
    # user inputs
    numTarget = input("How many targets per snapshot? (press enter for 1) >> ") 
    numTarget = 1 if numTarget == "" else int(numTarget)

    rotateTarget = True if input("Rotate target? (press enter for yes) >> ") == "" else False

    shapeColor = input("What shape color? (press enter for random) >> ")
    shapeColor = "random" if shapeColor == "" else shapeColor

    letter = input("What letter? (press enter for random) >> ")
    letter = "random" if letter == "" else letter

    letterColor = input("What letter color? (press enter for random) >> ")
    letterColor = "random" if letterColor == "" else letterColor

    print(numTarget, rotateTarget, shapeColor, letter, letterColor)

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

    # check if target practice directory exists
    if os.path.exists(vars.targetPracticeDir):
        rmtree(vars.targetPracticeDir)
    os.makedirs(vars.targetPracticeDir)

    # remove target_practice_info.csv if it exists
    if os.path.exists(vars.targetPracticeInfoPath):
        os.remove(vars.targetPracticeInfoPath)
    with open(vars.targetPracticeInfoPath, "w") as info:
        info.write("filename,shape,shapeColor,letter,letterColor\n")

    for filename in os.listdir(vars.noTargetDir):
        print(f"Simulating targets for {filename}")
        with Image.open(os.path.join(vars.noTargetDir, filename)) as snapshot:
            snapshot = snapshot.convert("RGBA")
            for i in range(numTarget):
                targetFilename = filename[:-4] + f"_tar_{i:03}"
                sim = SimImage(snapshot, targetFilename)
                sim.setTargetParams(rotateTarget, shapeColor, letter, letterColor)
                sim.practiceTarget()


if __name__ == "__main__":
    main()
