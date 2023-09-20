# imports
import os
from random import randint, choice

from PIL import Image, ImageDraw, ImageFont
from shapely import affinity
from shapely.geometry import box

import vars


# constants
SHAPES = (
    "triangle", "square", "pentagon", "hexagon", "heptagon",
    "octagon", "circle", "semicircle", "quartercircle",
    "rect", "star", "trap", "cross"
)
SPECIAL_CASES = ["semicircle", "quartercircle",
                 "rect", "star", "trap", "cross"]
POLYGONS = ["triangle", "square", "pentagon", "hexagon", "heptagon", "octagon"]

COLORS = {
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

CHARACTERS = (*list(range(48, 58)), *list(range(65, 91)))


# move polygon to a random location within image bounds
def moveTarget(polygon):
    xMin, yMin, xMax, yMax = [int(b) for b in polygon.bounds]
    width = xMax - xMin
    height = yMax - yMin

    # choose random location
    offset = [
        randint(0, vars.imageSizePx[0] - width),
        randint(0, vars.imageSizePx[1] - height),
    ]  # upper left corner of target

    # move to location
    polygon = affinity.translate(polygon, xoff=offset[0], yoff=offset[1])

    return polygon


# choose a color from colors, excluding if necessary
def chooseColor(exclude=None):
    validColors = list(COLORS.keys())
    if exclude:
        validColors = [c for c in validColors if c != exclude]

    return choice(validColors)


# create a seed for the target with some params specified
def generateSeed(params=None) -> dict:
    seed = {
        "rotation": None,
        "shape": None,
        "shapeColor": None,
        "letter": None,
        "letterColor": None,
    }

    if params:
        for k, v in params.items():
            if k == "rotate":
                seed["rotation"] = None if v else 0
            else:
                seed[k] = None if v == "random" else v

    if seed["rotation"] is None:
        seed["rotation"] = randint(0, 359)

    seed["shape"] = SHAPES[randint(0, 12)]

    if seed["shapeColor"] is None:
        seed["shapeColor"] = chooseColor(exclude=seed.get("letterColor"))

    if seed["letter"] is None:
        seed["letter"] = chr(CHARACTERS[randint(0, len(CHARACTERS) - 1)])

    if seed["letterColor"] is None:
        seed["letterColor"] = chooseColor(exclude=seed.get("shapeColor"))

    return seed


# draw shape on target
def drawShape(img, shape, color):
    draw = ImageDraw.Draw(img)

    if (shape == "circle"):
        draw.ellipse([0, 0, img.size], fill=COLORS[color], width=0)
    elif (shape in SPECIAL_CASES):
        with Image.open(vars.resourceDir + shape + ".bmp") as bitFile:
            scaleFactor = vars.targetSize[0] / bitFile.width
            newSize = [int(bitFile.width * scaleFactor),
                       int(bitFile.height * scaleFactor)]
            scaledBitFile = bitFile.resize(newSize)
            draw.bitmap([0, 0], scaledBitFile, fill=COLORS[color])
    else:
        draw.regular_polygon(
            [img.size[0] / 2, img.size[1] / 2, img.size[0] / 2],
            POLYGONS.index(shape) + 3,
            fill=COLORS[color]
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
        fill=COLORS[color],
        anchor="mm",
        font=font
    )

    return img


class SimImage:
    def __init__(self, s=None, f=None):
        self.snapshot = s.copy()
        self.filename = f
        self.targets = []

    def setTargetParams(self, rot, shpColor, ltr, ltrColor):
        self.seed = {
            "rotate": rot,
            "shapeColor": shpColor,
            "letter": ltr,
            "letterColor": ltrColor
        }

    def createTarget(self, **kwargs):
        seed = generateSeed(self.seed)

        # create a new image, draw shape and letter
        image = Image.new(mode="RGBA", size=vars.targetSize, color="#0000")
        image = drawShape(image, seed["shape"], seed["shapeColor"])
        image = drawLetter(image, seed["letter"], seed["letterColor"])

        # create a polygon for the target
        polygon = box(0, 0, image.size[0], image.size[1])

        # rotate the image
        image = image.rotate(
            seed["rotation"],
            expand=True,
            fillcolor="#0000"
        )

        # rotate the polygon (negative for different origin)
        polygon = affinity.rotate(polygon, -seed["rotation"])
        polygon = affinity.translate(
            polygon,
            xoff=-polygon.bounds[0],
            yoff=-polygon.bounds[1]
        )  # snap to axes

        self.targets.append({
            "image": image,
            "polygon": polygon,
            "seed": seed,
        })

    # returns a new Image of target placed on self.snapshot
    def placeTarget(self, i):
        t = self.targets[i]
        xMin, yMin, xMax, yMax = [int(b) for b in t["polygon"].bounds]
        self.snapshot.alpha_composite(t["image"], dest=(xMin, yMin))

    def saveSnapshot(self, location):
        self.snapshot.convert("RGB") \
            .save(os.path.join(location, self.filename + ".jpg"))

        with open(vars.targetPracticeInfoPath, "a") as info:
            for t in self.targets:
                seed = [str(i) for i in t["seed"].values()][1:]
                info.write(f"{self.filename},{','.join(seed)}\n")

    def cropSnapshot(self):
        if len(self.targets) != 1:
            print("error: len(targets) != 1")

        xMin, yMin, xMax, yMax = [int(b) for b in self.targets[0]["polygon"].bounds]
        self.snapshot = self.snapshot.crop((xMin - 15, yMin - 15, xMax + 15, yMax + 15))

    def practiceTarget(self):
        self.createTarget()
        self.targets[0]["polygon"] = moveTarget(self.targets[0]["polygon"])
        self.placeTarget(0)
        self.cropSnapshot()
        self.saveSnapshot(vars.targetPracticeDir)


if __name__ == "__main__":
    # small test of target practice
    for i in range(10):
        with Image.open(os.path.join(vars.noTargetDir, "img_000.jpg")) as s:
            s = s.convert("RGBA")
            simulate = SimImage(s, f"img_000_tar_00{i}")
            simulate.practiceTarget()

    # test letter generation
    for _ in range(100):
        print(generateSeed()["letter"])
