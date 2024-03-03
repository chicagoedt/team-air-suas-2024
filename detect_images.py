import sys
import cv2
from ultralytics import YOLO

sys.path.insert(0, "image-splitters")
from array_split import split_array, max_target_size
img_path = "./image-splitters/Targets/0_7.jpg" #Resolution: 4k by 3k
#img_path = "dog-puppy-on-garden-royalty-free-image-1586966191.jpg"
img_path = "./image-splitters/images_to_examine/white_octogon_black_2_green_pentagon_yellow_O.jpg"

yoloModel = YOLO("best.pt")
#yoloModel = YOLO("yolov8n.pt")

def getShape(value):
    shapes = {0: 'triangle', 1: 'pentagon', 2: 'circle', 3: 'semicircle', 4: 'quartercircle', 5: 'rectangle', 6: 'star', 7: 'cross'}
    return shapes[value]

def is_similar_spot(coord1, coord2):
    return True if (abs(coord1[0] - coord2[0]) <= max_target_size and abs(coord1[1] - coord2[1]) <= max_target_size) else False

def calculateAverage(points):
    totalx = 0
    totaly = 0
    shape = points[0][2] #Gets shape

    for point in points:
        totalx += point[0]
        totaly += point[1]
    
    return (totalx / len(points), totaly / len(points), shape)

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
    data_of_images = split_array(img)

    # yolo (np arrays)
    for data_of_image in data_of_images:
        sub_image = data_of_image[0]
        coordinates = data_of_image[1]
        x_offset = coordinates[0]
        y_offset = coordinates[1]
        # print("Offset: (" + str(x_offset) + ", " + str(y_offset) + ")")
        #Use YOLO to detect coordinates of target
        result_list = yoloModel(sub_image)
        
        for result in result_list:
            if len(result) != 0:
                #Adds coordinate in list
                properties = result.boxes.xywh[0]
                shape = getShape(int(result.boxes.cls.numpy()[0]))
                x = int(properties[0])
                y = int(properties[1])
                #print(str(x) + ", " + str(y) +", " + str(x_offset) +", " + str(y_offset))
                coordinate = (x + x_offset, y + y_offset, shape)
                coord_list.append(coordinate)
        
    if (len(coord_list) > 1):
        coord_list = removeDuplicates(coord_list)

    #Return coordinates of target (list of cordinate (which in turn are in tuples))
    return coord_list

if __name__ == "__main__":
    print(detectTarget(img_path))