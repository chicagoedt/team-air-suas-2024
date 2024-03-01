import sys
import cv2
from ultralytics import YOLO

sys.path.insert(0, "image-splitters")
from array_split import split_array
img_path = "./image-splitters/Targets/0_7.jpg" #Resolution: 4k by 3k
#img_path = "dog-puppy-on-garden-royalty-free-image-1586966191.jpg"

yoloModel = YOLO("best.pt")
#yoloModel = YOLO("yolov8n.pt")

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
        print("Offset: (" + str(x_offset) + ", " + str(y_offset) + ")")
        #Use YOLO to detect coordinates of target
        print(sub_image.shape)
        result_list = yoloModel(sub_image)
        
        for result in result_list:
            if len(result) != 0:
                #Adds coordinate in list
                box = result.boxes.xywh[0]
                #print(box)
                x = int(box[0])
                y = int(box[1])
                print(str(x) + ", " + str(y) +", " + str(x_offset) +", " + str(y_offset))
                coordinate = (x + x_offset, y + y_offset)
                coord_list.append(coordinate)

    #Return coordinates of target (list of cordinate (which in turn are in tuples))
    return coord_list

if __name__ == "__main__":
    print(detectTarget(img_path))