from PIL.ImageTransform import QuadTransform
from numpy import ravel
from shapely import affinity

import vars

# given the runway image, create a new image with the boundaries of the snapshot
def takePicture(runway, snapshot):
    snapshotCorners = ravel((snapshot.exterior.coords[3] + snapshot.exterior.coords[2] +
                            snapshot.exterior.coords[1] + snapshot.exterior.coords[0]))
    img = runway.transform(vars.imageSizePx, QuadTransform(snapshotCorners))
    return img


# shift the snapshot polygon down or to the right
def shiftSnapshot(snapshot):
    # shift the snapshot down, overlapping by 2 * target height
    newSnapshot = affinity.translate(
        snapshot,
        yoff=vars.snapshotHeight - (2 * vars.targetSize[1]) / vars.scaleFactor
    )

    # if moving down took us out of the boundary, move all the way up and right
    if not newSnapshot.intersects(vars.airDropBoundary):
        newSnapshot = affinity.translate(
            snapshot,
            xoff=vars.snapshotWidth -
            (2 * vars.targetSize[0]) / vars.scaleFactor,
            yoff=-snapshot.bounds[1] + vars.airDropBoundary.bounds[1]
        )

    # use new snapshot
    return newSnapshot
