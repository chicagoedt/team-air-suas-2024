import asyncio
from mavsdk import System

import flightHelper
import vars


async def run():

    # initialize drone and check if it is healthy
    drone = await flightHelper.initializeDrone()
    originalHeightAbs = await flightHelper.getOriginalHeightAbs(drone)
    flightHelper.waitTillInput(vars.CONTROL)

    # arm
    print("-- Arming")
    await drone.action.arm()
    flightHelper.waitTillInput(vars.CONTROL)

    # take off
    print("-- Take off")
    await flightHelper.takeOff(drone, vars.targetHeight)
    flightHelper.waitTillInput(vars.CONTROL)

    # land and disarm
    await flightHelper.landAndDisarm(drone)

if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())