from PIL.ImageTransform import QuadTransform
from numpy import ravel
from shapely import affinity
import random

import vars

# given the runway image, create a new image with the boundaries of the snapshot
def takePicture(runway, snapshot, size):
    snapshotCorners = ravel((snapshot.exterior.coords[3] + snapshot.exterior.coords[2] +
                            snapshot.exterior.coords[1] + snapshot.exterior.coords[0]))
    img = runway.transform(size, QuadTransform(snapshotCorners))
    return img

# get a random snapshot based on original snapshot
def getNewSnapshot(snapshot):
    # choose a random location in the image
    xOffset = random.randint(vars.airDropBoundary.bounds[0], vars.airDropBoundary.bounds[2] - vars.snapshotWidth)
    yOffset = random.randint(vars.airDropBoundary.bounds[1], vars.airDropBoundary.bounds[3] - vars.snapshotHeight)

    # get new snapshot by shifting original snapshot by offsets x and y
    newSnapshot = affinity.translate(snapshot, xoff=xOffset, yoff=yOffset)
    return newSnapshot

