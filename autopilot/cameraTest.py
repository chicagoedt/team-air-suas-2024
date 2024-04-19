"""
Mission: go to place of waypoints, take photo, rtl.
"""

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

        # TODO: take photo and for each photo export to .jpg and .txt

    flightHelper.waitTillInput(vars.CONTROL)

    # TODO: analyze photos, get coordinates of found target ..., export to .txt file

    # land & disarm
    await drone.action.return_to_launch()
    
    print("-- Disarm")
    await drone.action.disarm()

asyncio.run(main())
