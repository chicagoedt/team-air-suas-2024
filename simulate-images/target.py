import random

from PIL import Image, ImageDraw, ImageFont
from shapely import affinity
from shapely.geometry import box

import vars

# constants
YOLOs = {
    "triangle": 0,
    "pentagon": 1, 
    "circle": 2,
    "semicircle": 3,
    "quartercircle": 4,
    "rectangle": 5,
    "star": 6,
    "cross": 7
}

colors = {
    "white": (255, 255, 255),  # White
    "black": (0, 0, 0),  # Black
    "red": (255, 0, 0),  # Red
    "green": (0, 255, 0),  # Green
    "blue": (0, 0, 255),  # Blue
    "purple": (127, 0, 255),  # Purple
    "orange": (255, 127, 0),  # Orange
    "brown": (72, 59, 39),  # Brown
}

shapes = (
    "triangle",
    "pentagon", 
    "circle",
    "semicircle",
    "quartercircle",
    "rectangle",
    "star",
    "cross"
)

special_cases = ["semicircle",
                 "quartercircle",
                 "rectangle",
                 "star",
                 "cross"]

polygons = ["triangle",
            "pentagon", 
            ]


# create a rotated target image and polygon
def createTarget(seed):
    # choose shape, letter, colors, and rotation
    randColors = random.sample(list(colors.keys()), k=2)
    targetSeed = {
        "shape": seed[0],
        "shapeColor": seed[1],
        "letter": seed[2],
        "letterColor": seed[3],
        "rotation": seed[4]
    }

    # decide the seed of the target: shape, letter, color, rotation
    if targetSeed["rotation"] == True:
        targetSeed["rotation"] = random.randint(0, 359)

    if targetSeed["shape"] == "random":
        targetSeed["shape"] =  shapes[random.randint(0, 7)]

    if targetSeed["shapeColor"] == "random":
        targetSeed["shapeColor"] = randColors[0]

    if targetSeed["letter"] == "random":
        targetSeed["letter"] = chr(random.randint(65, 90))

    if targetSeed["letterColor"] == "random":
        targetSeed["letterColor"] = randColors[1]

    # create a new image, draw shape and letter
    target = Image.new(mode="RGBA", size=vars.targetSize, color="#0000")
    target = drawShape(target, targetSeed["shape"], targetSeed["shapeColor"])
    target = drawLetter(target, targetSeed["letter"], targetSeed["letterColor"], targetSeed["shape"])

    # create a polygon for the target
    polygon = box(0, 0, target.size[0], target.size[1])

    # rotate the target
    target = target.rotate(targetSeed["rotation"], expand=True, fillcolor="#0000")

    # rotate the polygon (negative for different origin)
    polygon = affinity.rotate(polygon, -targetSeed["rotation"])
    polygon = affinity.translate(
        polygon,
        xoff=-polygon.bounds[0],
        yoff=-polygon.bounds[1]
    )  # snap to axes

    return (target, polygon, targetSeed)


# draw shape on target
def drawShape(img, shape, color):
    draw = ImageDraw.Draw(img)

    if (shape == "circle"):
        diameter = img.size[1] if (img.size[0] > img.size[1]) else img.size[0]
        diameter -= 4
        # determine the place to draw so circle will be in the center of the img
        centerImg = (img.size[0] / 2, img.size[1] / 2)
        upperLeftCorner = (centerImg[0] - diameter / 2, centerImg[1] - diameter / 2)
        bottomRightCorner = (centerImg[0] + diameter / 2, centerImg[1] + diameter / 2)

        draw.ellipse([upperLeftCorner, bottomRightCorner], fill=colors[color], width=0)
    elif (shape in special_cases):
        with Image.open(vars.resourceDir + shape + ".bmp") as bitFile:
            scaleFactor = vars.targetSize[0] / bitFile.width
            newSize = [int(bitFile.width * scaleFactor),
                       int(bitFile.height * scaleFactor)]
            scaledBitFile = bitFile.resize(newSize)
            draw.bitmap([0, 0], scaledBitFile, fill=colors[color])
    else:
        # set up parameters for draw regular_polygon
        center = (img.size[0] / 2, img.size[1] / 2)
        radius = img.size[0] / 2
        numSides = 0
        if shape == "triangle":
            numSides = 3
            radius += 7 # make the triangle bigger to contain big letter such as W
        #If shape is a pentagon:
        else:
            numSides = 5
        
        # draw regular_polygon
        draw.regular_polygon(
            (center, radius),
            numSides,
            fill=color)

    return img


# draw letter on target
def drawLetter(img, letter, color, shape):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        vars.resourceDir + "arial.ttf", int(vars.targetSize[0] / 2))
    if shape == "star":
        draw.text(
            [vars.targetSize[0] / 2, vars.targetSize[1] / 2 + 8],
            letter,
            fill=colors[color],
            anchor="mm",
            font=font
        )
    else:
        draw.text(
            [vars.targetSize[0] / 2, vars.targetSize[1] / 2],
            letter,
            fill=colors[color],
            anchor="mm",
            font=font
        )

    return img


# move the target polygon to a random location within the snapshot
# returns None if the placement is invalid (< 30ft from t1)
def moveTarget(polygon, imgSize):
    xMin, yMin, xMax, yMax = [int(b) for b in polygon.bounds]
    targetWidth = xMax - xMin
    targetHeight = yMax - yMin

    # choose random location
    offset = [
        random.randint(0, imgSize[0] - targetWidth),
        random.randint(0, imgSize[1] - targetHeight),
    ]  # upper left corner of target

    # move to location
    polygon = affinity.translate(polygon, xoff=offset[0], yoff=offset[1])

    # check that it was placed at least 30 ft away from t1
    # if t1 != None:
    #     dist = t1.distance(polygon) / vars.pxPerFt
    #     if dist < 30:
    #         return None

    return polygon
