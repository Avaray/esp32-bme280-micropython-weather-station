# ID for your device 
DEVICE_ID = ""

# Use machine unique ID for the device ID
# If set to True the DEVICE_ID will be ignored
# https://docs.micropython.org/en/latest/library/machine.html#machine.unique_id
DEVICE_USE_MACHINE_ID = False

# SCL and SDA pins for the sensor
SENSOR_SCL_PIN = 22
SENSOR_SDA_PIN = 21

# Use Fahrenheit instead of Celsius for temperature
SENSOR_USE_FAHRENHEIT = False

# Include ESP32 raw temperature in the data sent to the server
# https://docs.micropython.org/en/latest/library/esp32.html#esp32.raw_temperature
SENSOR_INCLUDE_ESP32_TEMPERATURE = False

# List of known Wi-Fi networks
# You can specify multiple networks. The device will try to connect to them in order
# It will not connect to networks that are not on this list
NETWORKS = [
  {"ssid": "", "password": ""}
]

# List of servers (URL's to upload sensor readings; names are optional)
# You Need to specify protocol (http/https) in the URL
# Without specified protocol the request might not be sent
# You can specify multiple servers. The device will try to send readings to them in order
SERVERS = [
  {"name": "", "url": ""}
]

# Upload sensor readings to all servers from the list
# If set to False, the device will upload readings only to the first available server from the list
SERVERS_SEND_TO_ALL = False

# How often check readings and send them to server (in minutes)
# In other words, for how long to put the device to deep sleep
FREQUENCY = 15

# Enable or disable logs
LOGS_ENABLED = True

# Save logs on device
LOGS_SAVE = True

# Directory for log files (optional; default: logs)
LOGS_DIR = "logs"

# How many log files to keep on the device (optional; default: 20)
# Remember that space on the device is limited and you should keep this number low
LOGS_MAX_FILES = 20

# Enable or disable Over-The-Air updates 
# If enabled, the device will check for updates on start and download them if available
OTA_UPDATES = False

# By default the device will boot in Admin Mode when ADMIN_MODE_PIN_OUT and ADMIN_MODE_PIN_IN are connected (shorted)
# If you want to reverse this behavior, set ADMIN_MODE_REVERSED to True
ADMIN_MODE_REVERSED = False

# GPIO pins for Admin Mode
ADMIN_MODE_PIN_OUT = 17
ADMIN_MODE_PIN_IN = 16

# Wi-Fi SSID and password for Admin Mode (optional)
# Default SSID is "Weather Station" and password is not required
ADMIN_MODE_WIFI_SSID = ""
ADMIN_MODE_WIFI_PASSWORD = ""
