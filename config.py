# Name for your device (optional)
deviceId = ""

# List of Wi-Fi networks
# You can specify multiple networks. The device will try to connect to them in order
networks = [
  {"ssid": "", "password": ""}
]

# List of servers (URL's to upload sensor readings; names are optional)
# You Need to specify protocol (http/https) in the URL
# Without specified protocol the request might not be sent
# You can specify multiple servers. The device will try to send readings to them in order
servers = [
  {"name": "", "url": ""}
]

# SCL and SDA pins for BME280 sensor
BME280_SCL_PIN = 22
BME280_SDA_PIN = 21

# How often check readings and send them to server (in minutes)
# In other words, how often the device will wake up (from deep sleep) and send readings
frequency = 15
