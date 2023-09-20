'''
    a collection of hsv ranges of some colors
'''
import numpy as np

# color in competition: white, black, gray, red, blue, green, yellow, purple, brown, and orange
# hsv range????

# white
lower_white = np.array([0, 0, 215])
upper_white = np.array([180, 50, 255]) 
lowerWhite_array = [lower_white]
upperWhite_array = [upper_white]

# black
lower_black = np.array([0, 0, 0])   # from internet, needs checking
upper_black = np.array([180, 255, 30])
lowerBlack_array = [lower_black]
upperBlack_array = [upper_black]

# gray # no need to define this guy 

# red
lower_red1 = np.array([0, 180, 70])
upper_red1 = np.array([6, 255, 255])
lower_red2 = np.array([161, 180, 70]) # previously 157, 180, 70 but because of purple
upper_red2 = np.array([179, 255, 255])
lower_red3 = np.array([7, 200, 150])
upper_red3 = np.array([7, 255, 255])
lower_red4 = np.array([8, 220, 150])
upper_red4 = np.array([8, 255, 255])
lower_red5 = np.array([9, 230, 150])
upper_red5 = np.array([9, 255, 255])
lower_red6 = np.array([10, 245, 150])
upper_red6 = np.array([10, 255, 255])
lowerRed_array = [lower_red1, lower_red2, lower_red3, lower_red4, lower_red5, lower_red6]
upperRed_array = [upper_red1, upper_red2, upper_red3, upper_red4, upper_red5, upper_red6]

# blue
lower_blue = np.array([90, 100, 100])
upper_blue = np.array([130, 255, 255])
lowerBlue_array = [lower_blue]
upperBlue_array = [upper_blue]

# green
lower_green = np.array([44, 100, 70])
upper_green = np.array([80, 255, 255])
lowerGreen_array = [lower_green]
upperGreen_array = [upper_green]

# yellow
lower_yellow = np.array([26, 130, 150])
upper_yellow = np.array([33, 255, 255])
lowerYellow_array = [lower_yellow]
upperYellow_array = [upper_yellow]

# purple
lower_purple = np.array([132, 75, 75])
upper_purple = np.array([160, 255, 255])
lowerPurple_array = np.array([lower_purple])
upperPurple_array = np.array([upper_purple])

# brown 
lower_brown1 = np.array([12, 60, 40]) # need to check again to see if it covers some gray
upper_brown1 = np.array([20, 255, 149])
lower_brown2 = np.array([21, 60, 40])
upper_brown2 = np.array([25, 149, 149])
lowerBrown_array = [lower_brown1, lower_brown2]
upperBrown_array = [upper_brown1, upper_brown2]

# orange
lower_orange1 = np.array([11, 150, 150])
upper_orange1 = np.array([25, 255, 255])
lower_orange2 = np.array([7, 150, 150])
upper_orange2 = np.array([7, 199, 255])
lower_orange3 = np.array([8, 150, 150])
upper_orange3 = np.array([8, 219, 255])
lower_orange4 = np.array([9, 150, 150])
upper_orange4 = np.array([9, 229, 255])
lower_orange5 = np.array([10, 150, 150])
upper_orange5 = np.array([10, 244, 255])
lower_orange6 = np.array([4, 150, 150])
upper_orange6 = np.array([6, 179, 255])
lowerOrange_array = [lower_orange1, lower_orange2, lower_orange3, lower_orange4, lower_orange5, lower_orange6]
upperOrange_array = [upper_orange1, upper_orange2, upper_orange3, upper_orange4, upper_orange5, upper_orange6]


# dictionary color
colorDict = {
    'White': (lowerWhite_array, upperWhite_array),
    'Black': (lowerBlack_array, upperBlack_array),
    'Red': (lowerRed_array, upperRed_array),
    'Blue': (lowerBlue_array, upperBlue_array),
    'Green': (lowerGreen_array, upperGreen_array),
    'Yellow': (lowerYellow_array, upperYellow_array),
    'Purple': (lowerPurple_array, upperPurple_array),
    'Brown': (lowerBrown_array, upperBrown_array),
    'Orange': (lowerOrange_array, upperOrange_array),
}