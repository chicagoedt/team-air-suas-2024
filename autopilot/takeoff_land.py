import asyncio
from mavsdk import System

vim_address = "serial:///dev/ttyTHS1:57600"
droneHeight = 30
offset = 1
CONTROL = True

def waitTillInput():
    if CONTROL:
        input("Enter to continue next action ")


async def run():

    # initialize drone and check if it is healthy
    drone = System()
    await drone.connect()

    status_text_task = asyncio.ensure_future(print_status_text(drone))

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

    # set the takeoff altitude before arm
    takeoff_alt = await drone.action.get_takeoff_altitude()
    print("Take off original altitude:", takeoff_alt)
    await drone.action.set_takeoff_altitude(droneHeight)
    async for alt in drone.telemetry.altitude():
        original_alt = alt.altitude_relative_m
        break
    print("Original altitude:", original_alt)
    waitTillInput()

    # flying
    print("-- Arming")
    await drone.action.arm()
    waitTillInput()

    print("-- Taking off")
    await drone.action.takeoff()
    async for alt in drone.telemetry.altitude(): # take off to 30 m before doing next command
        currentAlt = alt.altitude_relative_m
        if currentAlt >= (droneHeight - offset):
            break
    waitTillInput()

    print("-- Landing")
    await drone.action.land()
    async for in_air in drone.telemetry.in_air():
        if not in_air:
            break
    
    print("-- Disarm")
    await drone.action.disarm()

    status_text_task.cancel()


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())