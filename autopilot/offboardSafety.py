"""
    This file is for testing the safety of the offboard
    The main question is whether we can flip offboard switch to manual to take manual control of the drone
"""

from mavsdk import System
import asyncio

import flightHelper

vim_address = "serial:///dev/ttyTHS1:57600"
droneHeight = 30
offset = 1
CONTROL = True

async def main():
    # initialize drone and check if it is healthy
    drone = flightHelper.initializeDrone()
    flightHelper.waitTillInput(CONTROL)

    # check if the drone is safe in offboard
    async for mode  in drone.telemetry.flight_mode():
        print("Mode:", mode)
        if mode == "OFFBOARD":
            print("-- it is in offboard mode!")
            break

    # check health of offboard mode
    offBoardActive = await drone.offboard.is_active()
    print("Offboard is active: ", offBoardActive)
    flightHelper.waitTillInput(CONTROL)

    # check arm and take off
    await drone.action.arm()
    flightHelper.waitTillInput(CONTROL)

    flightHelper.takeOff(drone, droneHeight)
    flightHelper.waitTillInput(CONTROL)

if __name__ == "__main__":
    asyncio.run(main())
