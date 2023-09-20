import random

from PIL import Image, ImageDraw, ImageFont
from shapely import affinity
from shapely.geometry import box

import vars

# constants
colors = {
    "white": (255, 255, 255),  # White
    "black": (0, 0, 0),  # Black
    "gray": (127, 127, 127),  # Gray
    "red": (255, 0, 0),  # Red
    "green": (0, 255, 0),  # Green
    "blue": (0, 0, 255),  # Blue
    "yellow": (255, 255, 0),  # Yellow
    "purple": (127, 0, 255),  # Purple
    "orange": (255, 127, 0),  # Orange
    "brown": (72, 59, 39),  # Brown
}

shapes = (
    "triangle", "square", "pentagon", "hexagon", "heptagon",
    "octagon", "circle", "semicircle", "quartercircle",
    "rect", "star", "trap", "cross"
)

special_cases = ["semicircle", "quartercircle",
                 "rect", "star", "trap", "cross"]
polygons = ["triangle", "square", "pentagon", "hexagon", "heptagon", "octagon"]


# create a rotated target image and polygon
def createTarget():
    # choose shape, letter, colors, and rotation
    randColors = random.sample(list(colors.keys()), k=2)
    seed = {
        "shape": shapes[random.randint(0, 12)],
        "shapeColor": randColors[0],
        "letter": chr(random.randint(65, 90)),
        "letterColor": randColors[1],
        "rotation": random.randint(0, 359)
    }

    # create a new image, draw shape and letter
    target = Image.new(mode="RGBA", size=vars.targetSize, color="#0000")
    target = drawShape(target, seed["shape"], seed["shapeColor"])
    target = drawLetter(target, seed["letter"], seed["letterColor"])

    # create a polygon for the target
    polygon = box(0, 0, target.size[0], target.size[1])

    # rotate the target
    target = target.rotate(seed["rotation"], expand=True, fillcolor="#0000")

    # rotate the polygon (negative for different origin)
    polygon = affinity.rotate(polygon, -seed["rotation"])
    polygon = affinity.translate(
        polygon,
        xoff=-polygon.bounds[0],
        yoff=-polygon.bounds[1]
    )  # snap to axes

    return (target, polygon, seed)


# draw shape on target
def drawShape(img, shape, color):
    draw = ImageDraw.Draw(img)

    if (shape == "circle"):
        draw.ellipse([0, 0, img.size], fill=colors[color], width=0)
    elif (shape in special_cases):
        with Image.open(vars.resourceDir + shape + ".bmp") as bitFile:
            scaleFactor = vars.targetSize[0] / bitFile.width
            newSize = [int(bitFile.width * scaleFactor),
                       int(bitFile.height * scaleFactor)]
            scaledBitFile = bitFile.resize(newSize)
            draw.bitmap([0, 0], scaledBitFile, fill=colors[color])
    else:
        draw.regular_polygon(
            [img.size[0] / 2, img.size[1] / 2, img.size[0] / 2],
            polygons.index(shape) + 3,
            fill=color
        )
    
    return img


# draw letter on target
def drawLetter(img, letter, color):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        vars.resourceDir + "arial.ttf", int(vars.targetSize[0] / 2))

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
def moveTarget(polygon, t1=None):
    xMin, yMin, xMax, yMax = [int(b) for b in polygon.bounds]
    targetWidth = xMax - xMin
    targetHeight = yMax - yMin

    # choose random location
    offset = [
        random.randint(0, vars.imageSizePx[0] - targetWidth),
        random.randint(0, vars.imageSizePx[1] - targetHeight),
    ]  # upper left corner of target

    # move to location
    polygon = affinity.translate(polygon, xoff=offset[0], yoff=offset[1])

    # check that it was placed at least 30 ft away from t1
    if t1 != None:
        dist = t1.distance(polygon) / vars.pxPerFt
        if dist < 30:
            return None

    return polygon
