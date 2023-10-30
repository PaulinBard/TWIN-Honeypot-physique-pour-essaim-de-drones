#!/usr/bin/env python3
import asyncio
from mavsdk import System
from mavsdk.server_utility import StatusTextType

"""
Fichier avec les commandes de bases du drone en udp avec mavsdk
changer le system adresse pour choisir le port du drone sur la machine
"""




system_address="udp://:14550"

async def connect():

    drone = System()
    await drone.connect(system_address)

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
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            await drone.server_utility.send_status_text(StatusTextType.INFO, "Hello world!")
            break
async def position():

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    async for position in drone.telemetry.position():
        print(position)
        return position
        break

async def arm():

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("-- Arming")
    await drone.action.arm()
async def disarm():

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("-- Arming")
    await drone.action.disarm()

async def takeoff():

    drone = System()
    await drone.connect(system_address)
    await drone.action.arm()
    status_text_task = asyncio.ensure_future(print_status_text(drone))
    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(10)
async def land():

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))
    print("-- Landing")
    await drone.action.land()

async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return



