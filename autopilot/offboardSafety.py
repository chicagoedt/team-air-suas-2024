"""
    This file is for testing the safety of the offboard
    The main question is whether we can flip offboard switch to manual to take manual control of the drone
"""

from mavsdk import System
import asyncio

vim_address = "serial:///dev/ttyTHS1:57600"
droneHeight = 30
offset = 1
CONTROL = True

def waitTillInput():
    if CONTROL:
        input("Enter to continue next action ")

async def main():
    # initialize drone and check if it is healthy
    drone = System()
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break
    waitTillInput()

    # check if the drone is safe in offboard
    async for mode  in drone.telemetry.flight_mode():
        print("Mode:", mode)
        if mode == "OFFBOARD":
            print("-- it is in offboard mode!")
            break

    # check health of offboard mode
    offBoardActive = await drone.offboard.is_active()
    print("Offboard is active: ", offBoardActive)


if __name__ == "__main__":
    asyncio.run(main())
