"""Configuration file.

+----------------+         +----------------+   UDP/  +----------------+
| client         |   UDP   | proxy          |   TCP   | drone          |
|                +--------->                +--------->                |
|                <---------+ PROXY_ADDRESS  <---------+ DRONE_ADDRESS  |
|                |         | PROXY_PORT     |         | DRONE_PORT     |
+----------------+         +----------------+         +----------------+

"""



# used by the client
PROXY_ADDRESS = "localhost" # used when sending to the proxy
PROXY_PORT    = 20001

# used by the proxy
DRONE_ADDRESS = "localhost"
DRONE_PORT    = 50051