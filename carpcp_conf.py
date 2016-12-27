# CarPCP settings
CARPCP_DIR = '/opt/carpcp'

# Log file
LOG_TIME = '%H:%M:%S'
LOG_FILE = '/tmp/carpcp.log'
LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
# Log level
#    10 - Debug
#    20 - Info
#    30 - Warning
#    40 - Error
#    50 - Fatal
LOG_LEVEL = 10

# Multicast settings
MULTICAST_PORT = 31337
MULTICAST_ADDR = '224.31.33.7'

# Serial port settings
SERIAL_SPEED = 100000
SERIAL_DEV = '/dev/ttyUSB0'

# WebServer settings
WEBSERVER_ADDR = '127.0.0.1'
WEBSERVER_PORT = 7350

# WebSocket settings
WEBSOCK_ADDR = 'ws://127.0.0.1:7350/ws'

# MPD Settings
MPD_PORT = 6600
MPD_ADDR = '127.0.0.1'
