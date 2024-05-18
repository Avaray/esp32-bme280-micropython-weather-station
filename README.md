# Weather Station for my Greenhouse (WIP)

![Image Description](/images/device.jpg)

# Hardware needed

- [ESP32](https://botland.store/1322-esp32-wifi-and-bt-modules) based development board.
- [BME280](https://botland.store/pressure-sensors/11803-bme280-humidity-temperature-and-pressure-5904422366179.html) sensor.
- Power supply, Powerbank (wuthout low current shutoff), or something else to power your device.
- Cables to connect things together.

# How to run code from this repository

1. Grab your ESP32 development board.
2. Connect BME280 sensor to proper Pins.
3. Upload all Python's `.py` files from this repository to your device (using [Thonny](https://thonny.org/) or [MPY-Jama](https://github.com/jczic/ESP32-MPY-Jama/releases)).
4. Configure device ([read below](https://github.com/Avaray/esp32-bme280-micropython-weather-station?tab=readme-ov-file#configuring-device)).
5. Reboot device and check terminal. Device will print messages on every important step (when booting, connecting to network, reading sensor, sending data, going to deep sleep). It will

# Configuring device

You need to modify `config.py` file to make it work.

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

# The Server

I have written server code in [Typescript](https://www.typescriptlang.org/) for [Bun.js](https://bun.sh/). For the database, I'm using [MongoDB](https://www.mongodb.com/). The code is created for my needs. I need to modify it before sharing.

# TODO's

**In the first place**

- Change the way how `config.py` is loaded
- Fix places in code where `config.deviceId` is used
- Do better connection handling

**Later**

- Do better keyboard interruptions. To have the ability to stop the program at any time. Currently, I have programmed it to work, but it can be done better. I need to think about it.
- Add the option to disable logging to save energy (does it make sense?).
- User Interface for Access Point mode. The user should have the ability to configure the device through a browser. This feature is to be implemented last as it is of low priority.
