import sys
import time
import cv2
import torch
import math

#Used to import Filepaths for Mac
import pathlib
from pathlib import Path
pathlib.WindowsPath = pathlib.PosixPath

#Imports the otehr modules from separate folders
sys.path.insert(0, "./image-splitters")
from array_split import split_array, max_target_size, showImage, max_sub_img_lw

#Import vars
import vars
from calc_distance import get_target_location

#Where the images we need to look at are
dir_path = "/Users/mightymanh/Desktop/myCode/team-air-suas-2024/odlc/target-detection/image-splitters/images_to_examine"

#Where the original YOLOv5 model is at (Currently local)
yolo_path = "/Users/mightymanh/yolov5"

#Current YOLO model (made from local yolo model)
model = torch.hub.load(yolo_path, 'custom', path='./best.pt', source='local', force_reload=True)


"""
Returns whether or not two coordinates are both looking at the
same target (Near the same target)

@param coord1 - 1st coordinate to look at
@param coord2 - 2nd coordinate to look at or compare to coord1
@returns true if cood1 and coord2 are pointing to the same target; otherwise false
"""
def is_similar_spot(coord1, coord2):
    return True if (abs(coord1[0] - coord2[0]) <= max_target_size and abs(coord1[1] - coord2[1]) <= max_target_size) else False

"""
Returns the average point given a bunch of points

@param points - list of points to average from
@returns the average point from the list of points provided
"""
"""
Returns the average point given a bunch of points

@param points - list of points to average from
@returns the average point from the list of points provided
"""
def calculateAverage(points):
    totalx = 0
    totaly = 0
    shape = points[0][2] #Gets shape

    #Sums up the x and y values of all points
    for point in points:
        totalx += point[0]
        totaly += point[1]
    
    #Returns average of x and y values from all points and adds shape at the end
    return (round(totalx / len(points)), round(totaly / len(points)), shape)

"""
Removes duplicate values

@param results - list of coordinates found from multiple images (could have duplicates)
@returns a new coordinates list without duplicate coordinates
"""
def removeDuplicates(results):
    index = 1

    #Use to store lists of values similar to each other
        #Key - value of original coordinate
        #Value - list of original coordinate and other ones in similar spot
    similar_values = {}

    #Stores values of original coordinates
    keys = []

    #Stores the final coordinates, which aren't duplicates
    final_coordinates = []

    #Iterate through elements
    for item in results:

        #Check if dictionary is empty
        if len(similar_values) == 0:
            #If it is, then add the first key to dictionary
            similar_values[item] = [item]
            keys.append(item)
        
        else:
            #Check which section item belongs in inside similar_values
            is_found = False
            #Iterate through keys
            for key in keys:
                #If a duplicate is found, put that in the corresponding list in similar_values
                is_found = is_similar_spot(item, key)
                if is_found:
                    similar_values[key].append(item)
                    break
            
            #If matching key is not found, make a new key for it
            if not is_found:
                similar_values[item] = [item]
                keys.append(item)

    #Get averages of elements in similar_values
    for key in keys:
        final_coordinates.append(calculateAverage(similar_values[key]))

    #Return final coordinates
    return final_coordinates

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return (qx, qy)

"""
Detects targets from a specific image and returns information about each target

@param path - path of image to look at
@returns a list of cooridnates in this format [(x, y, shape), (x1, y1, shape1)]
"""
def detectTarget(path, angle: int):
    # read the jpeg -> numpy array
    img = cv2.imread(path)

    img_dimensions = (len(img[0]), len(img))

    center_point = (img_dimensions[0]/2.0, img_dimensions[1]/2.0)

    #Stored coordinates (with shape)
    coord_list = []

    # split numpy array -> smaller np arrays
    data = split_array(img)

    #Iterates through smaller images found and data made:
    #In this format: [[img, img1], [(x, y), (x1, y1)]]
    for i in range(0, len(data[0])):
        #Gets image made at index i
        image = data[0][i]
        #Gets offset at index i  or (x, y)
        offset = data[1][i]
        #Feeds image into yolo model
        results = model(image)

        #Gets speific data from results made in model
        results_numpy = results.pandas().xyxy[0].to_numpy()  # Pandas DataFrame

        #Gets results of differetn targets found, and stores updated data in cooridnates
        for result in results_numpy:
            xmin = result[0]
            ymin = result[1]
            xmax = result[2]
            ymax = result[3]

            shape = result[6]
            #Center x point
            x = (xmax - xmin)/2 + xmin
            #Center y point
            y = (ymax - ymin)/2 + ymin
            #Final coordinate
            coordinate = (round(x + offset[0]), round(y + offset[1]), shape)

            if angle != 0:
                new_coord = rotate(center_point, (coordinate[0], coordinate[1]), (angle * math.pi / 180))
                final_coord = (new_coord[0], new_coord[1], coordinate[2])
                coord_list.append(final_coord)
            else:
                #Push coordinate to list
                coord_list.append(coordinate)
    
    #Remove duplicates made from list
    if (len(coord_list) > 1):
        coord_list = removeDuplicates(coord_list)

    #Return coordinates of target (list of cordinates which are in tuples)
    return coord_list

"""
Recreates image given information about target's location

@param img_path - stores path to original image
@param dimensions - stores dimensions (minx, maxX, miny, maxy) of image with target
@returns a list of images made that include targets in original pic
"""
def getImageWithTarget(img_path, dimensions : list):
    img = cv2.imread(img_path)
    images = []
    for dimension in dimensions:
        start_x = int(dimension[0])
        end_x = int(dimension[1])
        start_y = int(dimension[2])
        end_y = int(dimension[3])

        images.append(img[start_y:end_y, start_x:end_x])
    
    return images

"""
Gets list of image paths from directory path

@returns as shown above
"""
def getImagesGivenDirPath():
    #Finds files with .jpg at the end
    images = Path(dir_path).glob('*.jpg')
    imagePaths : list = []
    #Converts all file paths to string
    for image in images:
        imagePaths.append(str(image))
    return imagePaths

"""
Displays images of targets

@param img_path - path of original image
@param coord_list - list fo coordinates from original image
"""
def displaySubImages(img_path : str, coord_list : list):
    #Creates dimensions for images
    image_dimensions : list = []

    #Stores padding between point (320 px)
    offset = max_sub_img_lw/2

    #Coord format (x, y, s) - (x = x, y = y, s = shape)
    for coord in coord_list:
        #Format: (minx, maxX, miny, maxy)
        minx = coord[0] - offset
        maxx = coord[0] + offset
        miny = coord[1] - offset
        maxy = coord[1] + offset

        #If we end with negative values, we fix points
        if minx < 0:
            minx = 0
            maxx = max_sub_img_lw
        if miny < 0:
            miny = 0
            maxy = max_sub_img_lw

        image_dimensions.append((minx, maxx, miny, maxy))

    #Creates images based on file path and dimensions of each image
    images = getImageWithTarget(img_path, image_dimensions)

    #responsible for displaying images
    for i in range(0, len(images)):
        img = images[i]
        name = coord_list[i][2] + " " + str(coord_list[i][0]) + " - " + str(coord_list[i][1])
        showImage(img, name)

"""
Gets the data of text

@param - textPath of text file
@returns tuple in this format: (lat, lon, height, angle/yaw value)
"""
def getTextData(textPath: str):
    #Opens file
    file = open(textPath, "r")
    text : str = file.read()
    #Splits values in text file
    values : list = text.split(" ")

    #Converts all values from string to float
    for i in range(0, len(values)):
        values[i] = float(values[i])
    return values

"""
Gets file path and text file

@param - filepath of image file
@param - textPath of text file
@param - yawPath of yaw file
@returns data in this format: ([(x, y, s), (x1, y1, s1)], lat, lon, droneHeight)
"""
def someFunc(filePath: str, textPath: str):
    data = []

    #Gets variables x, y, h and puts it in data
    lat, lon, height, yawValue = getTextData(textPath)

    #Stores coordinates in list
    coord_list = detectTarget(filePath, yawValue)
    data.append(coord_list)

    #Displays sub images
    # displaySubImages(img_path, coord_list)

    data.append(lat)
    data.append(lon)
    data.append(height)

    #Returns the data in tuple format
    return tuple(data)

"""
    Converts coordinates in target to actual (lat, lon) coordinates

    @param data - stores data in this format: ([(x, y, s), (x1, y1, s1)], lat, lon, droneHeight)
    @retuns data in this new format: [(Lat, lon, s), (lat1, lon1, s1)]
"""
def getLatLonCoordinates(data : tuple):
    updated_data = []

    local_coords = data[0]
    local_lat = data[1]
    local_lon = data[2]
    local_height = data[3]
    vars.exportValuesDroneHeight(local_height)

    imgSizePx = vars.imageSizePx
    imgSizePxX = imgSizePx[0]
    imgSizePxY = imgSizePx[1]

    imgSizeFt = vars.imageSizeFt
    imgSizeFtX = imgSizeFt[0]
    imgSizeFtY = imgSizeFt[1]

    for coord in local_coords:
        x = coord[0]
        y = coord[1]
        shape = coord[2]
        new_coord = get_target_location(x, y, imgSizePxX, imgSizePxY, local_lat, local_lon, imgSizeFtX, imgSizeFtY)

        new_info = (new_coord[0], new_coord[1], shape)
        updated_data.append(new_info)
    
    return updated_data

"""

@assume - origianl distance is in feet
@feet should be 10.17
"""
def distanceBetweenTargets(point1, point2):
    distancePx = (((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2)) ** 0.5

    vars.exportValuesDroneHeight(75)

    distanceFt = distancePx / vars.pxPerFt
    print("Feet: " + str(distanceFt))
    print("Pixels: " + str(distancePx))

if __name__ == "__main__":
    #Gets each image path for every image in directory
    image_paths = getImagesGivenDirPath()

    for img_path in image_paths:
        #keeps track of time
        startTime = time.time()
        print(img_path)

        #Gets data needed for us ([Coordinates], x, y, droneHeight)
        textPath = str(img_path).replace(".jpg", ".txt")
        data = someFunc(img_path, textPath)
        print(data)

        new_data = getLatLonCoordinates(data)
        print(new_data)

        if len(new_data) > 0:
            for point in data[0]:
                distanceBetweenTargets(point, (vars.imageSizePx[0] / 2, vars.imageSizePx[1] / 2))

        #Also keeps track of time
        stopTime = time.time()
        print("Time taken: " + str((int)(stopTime - startTime)))
