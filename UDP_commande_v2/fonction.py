from pymavlink import mavutil
# from pymavlink.dialects.v20 import mavutil
import math
#!/usr/bin/env python3
import asyncio
from mavsdk import System
from mavsdk.server_utility import StatusTextType
import conf

# system adresses exemple:
#     system_address='udp://:14540'
#     system_address = f'udp://:{conf.DRONE_PORT}'

# connection exemple client:
#     proxy_address = f'udp:{conf.PROXY_ADDRESS}:{conf.PROXY_PORT}'
#     connection = mavutil.mavlink_connection(proxy_address)
# connection exemple server:
#     # Création de la connexion avec le numéro de système source = 1
#     connection = mavutil.mavlink_connection(
#     device=f'udpout:{conf.PROXY_ADDRESS}:{conf.PROXY_PORT}', source_system=source_sys)


# CONNECT SDK
async def async_connect(system_address):

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


def connect_sdk(system_address):
    asyncio.run(async_connect(system_address))
    print("drone connectsdk")

# ATTENTE DE ACK PYMAVLINK


def rep(connection, mavtype):
    msg = connection.recv_match(type=mavtype, blocking=True)
    print('message : '+str(msg))
    return msg


# ARM ALL
def arm(connection):
    print('arm...')
    connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                     0, 1, 0, 0, 0, 0, 0, 0)
    print('wait ack')
    rep(connection, 'COMMAND_ACK')


async def async_arm(system_address):

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("-- Arming")
    await drone.action.arm()


def arm_sdk(system_address):
    asyncio.run(async_arm(system_address))
    print("drone armsdk")

# DISARM ALL


def disarm(connection):
    print('disarm...')
    connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                     0, 0, 0, 0, 0, 0, 0, 0)
    rep(connection, 'COMMAND_ACK')


async def async_disarm(system_address):

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("-- Arming")
    await drone.action.disarm()


def disarm_sdk(system_address):
    asyncio.run(async_disarm(system_address))
    print("drone disarmsdk")


# TAKE OFF ALL
def takeoff(connection, hauteur):
    print('takeoff')
    connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                     # 0, 0, 0, 0, 0, 473977431, 85455947, 488180+hauteur)
                                     0, 0, 0, 0, 0, 0, 0, hauteur)
    msg=rep(connection, 'COMMAND_ACK')
    return msg


async def async_takeoff(system_address,hauteur=2.5):

    drone = System()
    await drone.connect(system_address)
    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("-- Arming")
    await drone.action.arm()
    status_text_task = asyncio.ensure_future(print_status_text(drone))
    print("-- Taking off")
    await drone.action.set_takeoff_altitude(hauteur)
    await drone.action.takeoff()
    await asyncio.sleep(10)


def takeoff_sdk(system_address,hauteur=2.5):
    asyncio.run(async_takeoff(system_address,hauteur))
    print("drone takeoffsdk")


# LAND ALL
def land(connection):
    print('land')
    connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_LAND,
                                     # 0, 0, 0, 0, 0, 473977431, 85455947, 488180+hauteur)
                                     0, 0, 0, 0, 0, 0, 0, 0)
    rep(connection, 'COMMAND_ACK')


async def async_land(system_address):

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))
    print("-- Landing")
    await drone.action.land()


def land_sdk(system_address):
    asyncio.run(async_land(system_address))
    print("drone landsdk")


# POSITION ALL
def position(connection):
    print('position')
    connection.mav.local_position_ned_send(0, 0, 0, 0, 0, 0, 0)
    rep(connection, 'LOCAL_POSITION_NED')
    rep(connection, 'COMMAND_ACK')


async def async_position(system_address):

    drone = System()
    await drone.connect(system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    async for position in drone.telemetry.position():
        # print(position.latitude_deg)
        # print(position.longitude_deg)
        # print(position.relative_altitude_m)
        lst = [position.latitude_deg, position.longitude_deg,
               position.relative_altitude_m]

        return lst
        break


def position_sdk(system_address):
    pos = str(asyncio.run(async_position(system_address)))
    return pos
    print("drone positionsdk")


def mode(connection, mode):
    connection.mav.set_mode_send(connection.target_system,
                                 mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                 connection.mode_mapping()[mode])

    rep(connection, 'COMMAND_ACK')


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return
