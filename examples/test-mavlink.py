#!/usr/bin/env python3
"""A simple script to test a mavlink connection.

This scripts sends a connect, arm and takeoff command to the drone.

Usage:
    python test-mavlink.py
"""

import mavsdk
import asyncio
import conf
import time

async def main():
    drone = mavsdk.System()

    #drone_address = f'udp://{conf.PROXY_ADDRESS}:{conf.PROXY_PORT}'
    drone_address='udp://:20001'
    print(f'connecting to {drone_address}')
    await drone.connect(drone_address)
    print(f'connected to  {drone._mavsdk_server_address}:{drone._port}')

    print('arming')
    await drone.action.arm()
    print('armed')

    print('takeoff')
    await drone.action.takeoff()
    print('took off')


if __name__ == '__main__':
    asyncio.run(main())