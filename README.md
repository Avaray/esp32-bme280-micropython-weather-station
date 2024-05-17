# Small project for my Greenhouse

# Hardware needed

- [ESP32](https://botland.store/1322-esp32-wifi-and-bt-modules) based development board.
- [BME280](https://botland.store/pressure-sensors/11803-bme280-humidity-temperature-and-pressure-5904422366179.html) sensor.
- Power supply, Powerbank (wuthout low current shutoff), or something else to power your device.

# How to run code from this repository

1. Grab your ESP32 device.
2. Connect BME280 sensor to proper Pins.
3. Upload files from this repository to your device (with [Thonny](https://thonny.org/) or [MPY-Jama](https://github.com/jczic/ESP32-MPY-Jama/releases)).
4. Configure device (read below).
5. Reboot device.

# Configuring device

You need to create and upload `config.py` file to your device.  
For the safety reasons it is not included in this repository.

```python
# Name for your device (optional)
deviceId = ""

# List of Wi-Fi networks
networks = [
  {"ssid": "My-Awesome-Network-Name", "password": "neverGuess123"}
]

# List of servers (URL's to upload sensor readings; names are optional)
servers = [
  {"name": "primary", "url": "https://my.website.com"},
  {"name": "local", "url": "http://192.168.0.20:4000"},
]

# SCL and SDA pins for BME280 sensor
BME280_SCL_PIN = 22
BME280_SDA_PIN = 21

# How often check readings and send them to server (in minutes)
frequency = 15
```

# Server

There are two options.

1. You can run very simple server with BUN.js by running command... `command will be here`
2. Full server is [available here](https://github.com/Avaray/weather-server-bun).

# TODO's

...
