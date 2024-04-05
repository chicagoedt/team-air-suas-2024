import asyncio
from mavsdk import System

vim_address = "serial:///dev/ttyTHS1:57600"

async def main():
    drone = System()

    print('Wating for drone connect')
    await drone.connect(vim_address)

    # checking if drone is connected
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"connected!")
            break
    
    async for

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")

asyncio.run(main())