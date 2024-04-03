import asyncio
from mavsdk import System
from mavsdk.server_utility import StatusTextType
from mavsdk.offboard import Offboard, OffboardError, VelocityNedYaw
import time

async def run():

    drone = System(sysid = 1)
    await drone.connect(system_address="serial:///dev/ttyTHS1:57600")
    print("Waiting for drone ...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("drone is connected")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    # arm
    print("-- Arming")
    await drone.action.arm()
    time.sleep(3)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())