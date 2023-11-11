import cv2
# import os
from pathlib import Path
import numpy as np
from PIL import Image
import shapely as sh

# coordinates = (
#     #Layer 1
#     (108, 240), (748, 240), (1388, 240), (2028, 240), (2668, 240), (3308, 240),
#     (108, 880), (748, 880), (1388, 880), (2028, 880), (2668, 880), (3308, 880),
#     (108, 1520), (748, 1520), (1388, 1520), (2028, 1520), (2668, 1520), (3308, 1520),
#     (108, 2160), (748, 2160), (1388, 2160), (2028, 2160), (2668, 2160), (3308, 2160),
#     #Layer 2
#     (0, 0), (640, 0), (1280, 0), (2136, 0), (2776, 0), (3415, 0),
#     (0, 640), (640, 640), (1280, 640), (2136, 640), (2776, 640), (3415, 640),
#     (0, 1760), (640, 1760), (1280, 1760), (2136, 1760), (2776, 1760), (3415, 1760),
#     (0, 2400), (640, 2400), (1280, 2400), (2136, 2400), (2776, 2400), (3415, 2400),
#     #Layer 3
#     (1708, 0), (1708, 640), (1708, 1200), (1708, 1760), (1708, 2400),
#     (0, 1200), (640, 1200), (1280, 1200), (2136, 1200), (2776, 1200), (3416, 1200)
# )
#
# img = cv2.imread('img_004_tar_000.jpg')
# print(img.shape)
# cv2.imshow("original", img)
#
# for coord in coordinates:
#     x = coord[0]
#     xend = x + 640
#     y = coord[1]
#     yend = y + 640
#     filename = "chunks2/" + str(x) + "_" + str(y) + ".jpg"
#     cropped = img[y:yend, x:xend]
#     cv2.imwrite(filename, cropped)
#
# cv2.waitKey(0)

#cropped = image[100:740, 100:740]
#cv2.imshow("Cropped", cropped);
#cv2.imwrite('chunks/newchair.jpg', cropped)
#cv2.waitKey(0);



def crop_img(image, crop_size: list,yoloInfo,id = 0, num_imgs = None):
    num_x_splits = int(np.ceil(image.size[0]/crop_size[0]))
    num_y_splits = int(np.ceil(image.size[1] / crop_size[1]))
    offset_x = np.ceil(abs(image.size[0] - num_x_splits * crop_size[0]) / (num_x_splits - 1))
    offset_y = np.ceil(abs(image.size[1] - num_y_splits * crop_size[1]) / (num_y_splits - 1))
    x_coords = [0] + [(crop_size[0] - offset_x) * x for x in range(1,num_x_splits)]
    y_coords = [0] + [crop_size[1] * y - offset_y * y for y in range(1,num_y_splits)]

    # Convert Annotations
    center_x = yoloInfo[0] * image.size[0]
    center_y = yoloInfo[1] * image.size[1]
    width = yoloInfo[2] * image.size[0]
    height = yoloInfo[3] * image.size[1]

    # Convert to Pixels
    bbox = [int(center_x - width/2),  #Left
            int(center_y + height / 2),  # Top
            int(center_x + width/2),  #Right
            int(center_y - height / 2)] #Bottom

    bbox = sh.Polygon([(bbox[0],bbox[1]), #TL
                       (bbox[2],bbox[1]), #TR
                       (bbox[2],bbox[3]), #BL
                       (bbox[0],bbox[3]),]) #BR



    print(f"x_coords:    {x_coords}")
    print(f"y_coords:    {y_coords}")

    for ind_x,x in enumerate(x_coords):
        for ind_y,y in enumerate(y_coords):

            left = x
            top = y
            right = x + crop_size[0]
            bottom = y + crop_size[1]
            region = sh.Polygon([(left,top),
                                 (right,top),
                                 (right,bottom),
                                 (left,bottom),])
            folder = Path(f"snapshots/chunks/chunks{id}")
            filename = folder / f"{ind_x}_{ind_y}"
            crop_img = image.crop((left, top, right, bottom))
            new_bbox = check_within(bbox, region)
            if new_bbox :
                coords = sh.get_coordinates(region)
                offset_x = coords[0,0]
                offset_y = coords[0, 1]
                bbox_trans = [new_bbox[0]-offset_x,
                              new_bbox[1]-offset_y,
                              new_bbox[2]-offset_x,
                              new_bbox[3]-offset_y,]
                width = (bbox_trans[2] - bbox_trans[0])/crop_size[0]
                height = (bbox_trans[3] - bbox_trans[1])/crop_size[1]
                center_x = ((bbox_trans[2] + bbox_trans[0]) / 2) / crop_size[0]
                center_y = ((bbox_trans[3] + bbox_trans[1]) / 2) / crop_size[1]

                trans_yolo = [0, center_x, center_y, width, height]

                # new_bbox_coords = [(x - offset_x, y - offset_y) for x,y in bbox_coords]
                # new_bbox = sh.transform(lambda x, y: (x - offset_x, y + offset_y), new_bbox)
                print(f"Write the saving function:  {trans_yolo}  {filename}")
                list_str = ' '.join(map(str, trans_yolo))
                # Write the string to the file
                with open(f"{filename}.yolo", 'w') as file:
                    file.write(list_str)


            print(f"Filename: {filename}")
            folder.mkdir(parents=True, exist_ok=True)
            if any(folder.iterdir()):
                print(f"Error: The directory contains image files: {folder}")

            crop_img.save(f"{filename}.jpg")



def check_within( bbox, region):
    is_within = sh.contains(region, bbox)
    print(bbox)
    if(is_within):
        return bbox.bounds
    elif bbox.intersects(region):
        return (bbox.intersection(region)).bounds
    else:
        return None


def test_check_within():
    # Test case 1: Completely within
    bbox = sh.Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])
    region = sh.Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
    result = check_within(bbox, region)
    print(result)
    # assert result.equals(bbox), "Test case 1 failed"

    # Test case 2: Partially within
    bbox = sh.Polygon([(2, 2), (2, 5), (3, 5), (3, 2)])
    region = sh.Polygon([(1, 1), (1, 4), (4, 4), (4, 1)])
    result = check_within(bbox, region)
    print(result)
    # assert result.equals(bbox.bounds), "Test case 2 failed"

    # Test case 3: Not within
    bbox = sh.Polygon([(5, 5), (5, 6), (6, 6), (6, 5)])
    region = sh.Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
    result = check_within(bbox, region)
    # assert result is None, "Test case 3 failed"
    print(result)
    # Test case 4: Bounding box completely within a larger region
    bbox = sh.Polygon([(1, 1), (1, 3), (3, 3), (3, 1)])
    region = sh.Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
    result = check_within(bbox, region)
    # assert result.equals(bbox), "Test case 4 failed"
    print(result)
    # Test case 5: Bounding box completely within a larger region (reversed order)
    bbox = sh.Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
    region = sh.Polygon([(1, 1), (1, 3), (3, 3), (3, 1)])
    result = check_within(bbox, region)
    # assert result.equals(region), "Test case 5 failed"
    # print(result)
    # print("All test cases passed")


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            print(file_content)
            file_content = [float(item) for item in file_content.split()]
            file_content.pop(0)
            return file_content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:
file_path = 'C://Users//yugio//Code//team-air-suas-2024//simulate-images//Test4k.yolo'
file_content = read_file(file_path)
img = Image.open("C://Users//yugio//Code//team-air-suas-2024//simulate-images//Test4k.jpg")
crop_size = [640,640]

crop_img(img, crop_size, file_content)

# test_check_within()
