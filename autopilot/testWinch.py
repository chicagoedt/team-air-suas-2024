"""
    Testing winch: to turn on winch, flip switch to HOLD mode
"""
from mavsdk import System, telemetry
import asyncio
import Jetson.GPIO as GPIO
import time

# setup arduino pin
arduino_pin = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(arduino_pin, GPIO.OUT, initial = GPIO.LOW)

# the idea is: first we fly with manual mode. Then whenever we change to stabilized mode, we do the airdrop

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
    
    # check mode
    print('Waiting for flight mode to change to HOLD mode then do airdrop')
    
    # get the previous flight mode
    previous_mode = 'unknown'
    async for flight_mode in drone.telemetry.flight_mode():
        previous_mode = str(flight_mode)
        if previous_mode != 'HOLD':
            break
        else:
            print('Make sure you set the flight mode different than HOLD')

    # switch: if it is in 'STABILIZE' mode, activate the arduino pin. else, deactivate the arduino pin HAHAHAHA
    async for flight_mode in drone.telemetry.flight_mode():
        current_mode = str(flight_mode)
        print('Previous mode: {}, Current mode: {}'.format(previous_mode, current_mode))
        if current_mode == previous_mode:
            print('Nothing change')
        elif str(flight_mode) == 'HOLD':
            previous_mode = 'HOLD'
            # turn on arduino code
            print('Turn on Arduino')
            GPIO.output(arduino_pin, GPIO.HIGH)
            print('arduino is ON!')
            #time.sleep(0.1)
            #print('done sleeping')
            #GPIO.output(arduino_pin, GPIO.LOW)
            #print('turn off arduino pin')
        else:
            previous_mode = current_mode
            # turn off arduino code
            print('Turn off Arduino')
            GPIO.output(arduino_pin, GPIO.LOW)
            print('arduino is OFF!')

asyncio.run(main())