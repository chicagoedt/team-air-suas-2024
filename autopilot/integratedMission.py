
#### Before running the program #####
# store the info of bottle to a global variable BOTTLE_TARGET

##### Running the program #####
# flight check: waypoints flying around

# our drone enters the airdrop area, scan the area to locate target
    # for each point that it reaches:
        # set drone to hover

        # take photo, gps coordinates: analyze it immediately (object detection).
            # if we found a target:
                # store info about target into csv file "found_targets.csv": shape, coordinate
            # if we dont found a target:
                # do nothing

        # move to next point

# for all found targets, match the one with that global variable BOTTLE_TARGET; get the coordinate

# go to that target, and airdrop