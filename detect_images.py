import sys
import cv2
import torch

#Used to import Mac
import pathlib
from pathlib import Path
pathlib.WindowsPath = pathlib.PosixPath

sys.path.insert(0, "image-splitters")
from array_split import split_array, max_target_size, showImage, max_sub_img_lw
dir_path = "./image-splitters/images_to_examine"
#img_path = "./image-splitters/images_to_examine/Frame-18-02-2023-04-59-12.jpg" #Resolution: 4k by 3k
# #img_path = "dog-puppy-on-garden-royalty-free-image-1586966191.jpg"
# img_path = "./image-splitters/images_to_examine/white_octogon_black_2_green_pentagon_yellow_O.jpg"

model = torch.hub.load('/Users/ethanky/Documents/GitHub/yolowv5/yolov5', 'custom', path='/Users/ethanky/Documents/GitHub/team-air-suas-2024/best.pt', source='local', force_reload=True)  # local model
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # local model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

#def getShape(value):
#    shapes = {0: 'triangle', 1: 'pentagon', 2: 'circle', 3: 'semicircle', 4: 'quartercircle', 5: 'rectangle', 6: 'star', 7: 'cross'}
#    return shapes[value]

def is_similar_spot(coord1, coord2):
    return True if (abs(coord1[0] - coord2[0]) <= max_target_size and abs(coord1[1] - coord2[1]) <= max_target_size) else False

def calculateAverage(points):
    totalx = 0
    totaly = 0
    shape = points[0][2] #Gets shape

    for point in points:
        totalx += point[0]
        totaly += point[1]
    return (round(totalx / len(points)), round(totaly / len(points)), shape)

def removeDuplicates(results):
    index = 1
    similar_values = {}
    keys = []
    final_coordinates = []

    #Iterate through elements
    for item in results:
        #Check if dictionary is empty
        if len(similar_values) == 0:
            similar_values[item] = [item]
            keys.append(item)
        else:
            #Check which section item belongs in inside similar_values
            is_found = False
            #Iterate through keys
            for key in keys:
                #If corresponding key is found, put that in
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

    return final_coordinates

# def getShape(shape):
#     if shape == 

def detectTarget(path):
    # read the jpeg -> numpy array
    img = cv2.imread(path)
    #to_dir = "./image-splitters/images"
    #imagePaths = splitImages(img, 0, toDirectory)
    coord_list = []

    # split numpy array -> smaller np arrays
    data = split_array(img)
    for i in range(0, len(data[0])):
        image = data[0][i]
        offset = data[1][i]
        results = model(image)
        # print("Results for " + str(i) + ":")
        # print(results)
        results_numpy = results.pandas().xyxy[0].to_numpy()  # Pandas DataFrame

        #Gets results, and stores updated data in cooridnates
        for result in results_numpy:
            # print("Result:")
            # print(result)
            xmin = result[0]
            ymin = result[1]
            xmax = result[2]
            ymax = result[3]
            shape = result[6]
            x = (xmax - xmin)/2 + xmin
            y = (ymax - ymin)/2 + ymin
            coordinate = (round(x + offset[0]), round(y + offset[1]), shape)
            coord_list.append(coordinate)
        
    if (len(coord_list) > 1):
        coord_list = removeDuplicates(coord_list)

    #Return coordinates of target (list of cordinate (which in turn are in tuples))
    return coord_list

#Creates new images with dimensions provided
    #@param tuple - stores dimensions (minx, maxX, miny, maxy)
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

def getImagesGivenDirPath():
    images = Path(dir_path).glob('*.jpg')
    imagePaths : list = []
    for image in images:
        imagePaths.append(str(image))
    return imagePaths

def displaySubImages(img_path : str):
    #Stores coordinates in list
    coord_list = detectTarget(img_path)
    print(coord_list)

    #Creates dimensions for image
    image_dimensions : list = []
    offset = max_sub_img_lw/2
    #Coord format (x, y, s) - (x = x, y = y, s = shape)
    for coord in coord_list:
        #Format: (minx, maxX, miny, maxy)
        minx = coord[0] - offset
        maxx = coord[0] + offset
        miny = coord[1] - offset
        maxy = coord[1] + offset
        if minx < 0:
            minx = 0
            maxx = max_sub_img_lw
        if miny < 0:
            miny = 0
            maxy = max_sub_img_lw


        image_dimensions.append((minx, maxx, miny, maxy))
    
    images = getImageWithTarget(img_path, image_dimensions)

    for i in range(0, len(images)):
        img = images[i]
        name = coord_list[i][2] + " " + str(coord_list[i][0]) + " - " + str(coord_list[i][1])
        showImage(img, name)

if __name__ == "__main__":
    # path = "image-splitters/images_to_examine/Frame-18-02-2023-05-00-10.jpg"
    # displaySubImages(path)
    image_paths = getImagesGivenDirPath()

    for img_path in image_paths:
        print(img_path)
        displaySubImages(img_path)
