'''
    Break a jpeg array into smaller jpeg arrays
'''
import cv2

max_sub_img_lw = 640
max_target_size = 118 #Size of target

#Shows images
def showImage(img):
    #Shows images
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

#Splits array
def split_array(big_JPEG_array):
    sub_arrays = [] #Stores image, and offset
    max_rows = len(big_JPEG_array)
    max_cols = len(big_JPEG_array[0])

    start_x = 0
    end_x = 0
    start_y = 0
    end_y = 0

    #Bool variables for when iterator is off limits (x and y)
    should_x_break = 0
    should_y_break = 0 

    #Iterate through cols
    while start_y < max_rows:
        end_y = start_y + max_sub_img_lw
        #If within y range
        # if end_y >= max_rows:
        #     #Set range of x
        #     end_y = max_rows
        #     new_y_start = end_y - max_sub_img_lw
        #     start_y = 0 if (new_y_start < 0) else new_y_start
        #     should_y_break = 1

        #Iterate through rows
        while start_x < max_cols:
            end_x = start_x + max_sub_img_lw
            #If within x range
            # if end_x >= max_cols:
            #     #Set range of x
            #     end_x = max_cols
            #     new_x_start = end_x - max_sub_img_lw
            #     start_x = 0 if (new_x_start < 0) else new_x_start
            #     should_x_break = 1

            #Get pixels of sub image
            #print("sub-images: (" + str(start_x) + ", " + str(end_x) + ") (" + str(start_y) + ", " + str(end_y) + ")")
            sub_array = big_JPEG_array[start_y:end_y, start_x:end_x]
            #Shows images
            showImage(sub_array)
            #print("Sub-array dimensions: height - " + str(len(sub_array)) + " width - " + str(len(sub_array[0])) )
            sub_arrays.append((sub_array, (start_x, start_y)))
            start_x += max_sub_img_lw - max_target_size
            if (should_x_break == 1):
                should_x_break = 0
                break
        start_y += max_sub_img_lw - max_target_size
        start_x = 0
        if (should_y_break == 1):
            should_y_break = 0
            break
    return sub_arrays