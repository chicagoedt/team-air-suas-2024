from mavsdk import System
import asyncio
import math

import flightHelper

vim_address = "serial:///dev/ttyTHS1:57600"
targetHeight = 30
CONTROL = False

# Convert feet to degrees
latitude_per_foot = 1.0/364000
longitude_per_foot = 1.0/288200

# MAIN FLYING
async def main():
    drone = await flightHelper.initializeDrone()
    originalHeightAbs = await flightHelper.getOriginalHeightAbs(drone)
    flightHelper.waitTillInput(CONTROL)

    # arm
    print("-- Arming")
    await drone.action.arm()
    flightHelper.waitTillInput(CONTROL)

    # take off
    await flightHelper.takeOff(drone, targetHeight)
    flightHelper.waitTillInput(CONTROL)

    # travel to first waypoint
    await flightHelper.goToWaypoint(drone, (41.8518786, -87.8294878), originalHeightAbs + targetHeight)

    # travel to second waypoint
    await flightHelper.goToWaypoint(drone, (41.8517664, -87.8289776), originalHeightAbs + targetHeight)
    flightHelper.waitTillInput(CONTROL)

    # land & disarm
    await flightHelper.land(drone)
    
    print("-- Disarm")
    await drone.action.disarm()

asyncio.run(main())