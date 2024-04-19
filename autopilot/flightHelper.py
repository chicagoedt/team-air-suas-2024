from mavsdk import System
import math
import asyncio

latitude_per_foot = 1.0/364000
longitude_per_foot = 1.0/288200

# function to enable slow control from user
def waitTillInput(CONTROL):
    if CONTROL:
        input("Enter to continue next action ")

# initialize the drone and wait until it is healthy
async def initializeDrone(address=None):
    # initialize drone
    drone = System()
    print("-- Attempting to connect to address:", address)
    if address == None:
        await drone.connect()
    else:
        await drone.connect(address)

    # check health
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    return drone

# get original drone height
async def getOriginalHeightAbs(drone):
    print("Fetching amsl altitude at home location...")
    async for terrain_info in drone.telemetry.home():
        originalHeightAbs = terrain_info.absolute_altitude_m
        print("original abs altitude:", originalHeightAbs)
        break
    
    return originalHeightAbs

# take off to global variable targetHeight
async def takeOff(drone, targetHeight):
    print("-- Taking off")
    await drone.action.takeoff()
    async for alt in drone.telemetry.altitude(): # take off to 30 m before doing next command
        currentAlt = alt.altitude_relative_m
        if currentAlt >= targetHeight - 1:
            break

# go to a waypoint
async def goToWaypoint(drone, waypoint, heightAbs, yaw=0):
    print("-- Traveling to waypoint:", waypoint)
    await drone.action.goto_location(waypoint[0], waypoint[1], heightAbs, yaw)
    async for position in drone.telemetry.position():
        distanceLat = (position.latitude_deg - waypoint[0]) / latitude_per_foot
        distanceLong = (position.longitude_deg - waypoint[1]) / longitude_per_foot
        distance = math.sqrt(distanceLat ** 2 + distanceLong ** 2)
        print(distance)
        if distance < 7:
            break

# land and disarm
async def land(drone):
    print("-- Landing")
    await drone.action.land()
    async for in_air in drone.telemetry.in_air():
        if not in_air:
            break