from mavsdk import System
import asyncio

import flightHelper
import vars

# MAIN FLYING
async def main():
    # initialize the drone
    drone = await flightHelper.initializeDrone()
    originalHeightAbs = await flightHelper.getOriginalHeightAbs(drone)
    flightHelper.waitTillInput(vars.CONTROL)

    # arm
    print("-- Arming")
    await drone.action.arm()
    flightHelper.waitTillInput(vars.CONTROL)

    # take off
    await flightHelper.takeOff(drone, vars.targetHeight)
    flightHelper.waitTillInput(vars.CONTROL)

    # waypoint travels
    for wp in vars.wpList:
        # travel to waypoint
        await flightHelper.goToWaypoint(drone, wp, originalHeightAbs + vars.targetHeight) # always make yaw points to 0
    flightHelper.waitTillInput(vars.CONTROL)

    # rtl & disarm
    print("-- Return to launch!")
    await drone.action.return_to_launch() # return to takeoff position. Dont know how to set it to other location
    
    print("-- Disarm")
    await drone.action.disarm()

asyncio.run(main())