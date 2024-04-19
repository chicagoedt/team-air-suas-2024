"""
Hyper parameters for offboard control are modified here
"""

# vehicle address for mavlink connection
vim_address = "serial:///dev/ttyTHS1:57600"

# geo facts
latitude_per_foot = 1.0/364000
longitude_per_foot = 1.0/288200

# mission params
targetHeight = 30 # m
offsetHeight = 1 # m
offsetWp = 7 # ft

# coordinates
wpList = [(41.8518786, -87.8294878), (41.8517664, -87.8289776)] # (lat, long)
rtlPoint = None # set to default takeoff positition

# computer
arduino_pin = 7 # for winch
    # for camera

# DEBUG variable
CONTROL = False