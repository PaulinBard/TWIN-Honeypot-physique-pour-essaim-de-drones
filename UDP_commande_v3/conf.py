"""Configuration file.

+----------------+         +----------------+         +----------------+
| client         |pymavlink| proxy_pilote   |         | drone          |
|                +--------->                +--------->                |
|                <---------+ PROXY_ADDRESS  <---------+ DRONE_ADDRESS  |
|                |         | PROXY_PORT     |         | DRONE_PORT     |
+----------------+         +-----^--+-------+         +----------------+
                    pymavlink    |  |           mavsdk
                           +-----+--v-------+         +----------------+
                           | proxy_sec      |         | drone2         |
                           |                +--------->                |
                           | PROXY2_ADDRESS <---------+ DRONE_ADDRESS2 |
                           | PROXY2_PORT    |         | DRONE_PORT2    |
                           +----------------+         +----------------+
"""


# used by the client
PROXY_ADDRESS = "localhost"  # used when sending to the proxy
PROXY_PORT = 20001
#used by the proxy
PROXY2_ADDRESS = "localhost"  # used when sending to the drone2
PROXY2_PORT = 20002
# used by the proxy
DRONE_ADDRESS = "localhost"
DRONE_PORT = 14550
# used by the proxy
DRONE_ADDRESS2 = DRONE_ADDRESS
DRONE_PORT2    = 14540
