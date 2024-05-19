# Name for your device (optional)
DEVICE_ID = ""

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

# SCL and SDA pins for BME280 sensor
BME280_SCL_PIN = 22
BME280_SDA_PIN = 21

# How often check readings and send them to server (in minutes)
# In other words, how often the device will wake up (from deep sleep) and send readings
FREQUENCY = 15

# Enable or disable logs
LOGS_ENABLED = True

# Save logs on device
LOGS_SAVE = True

# Directory for log files (optional; default: logs)
LOGS_DIR = "logs"

# How many log files to keep on the device (optional; default: 20)
LOGS_MAX_FILES = 20

# Enable or disable OTA updates (disabled by default)
# If enabled, the device will check for updates on start and download them if available
UPDATE_ON_START = False
