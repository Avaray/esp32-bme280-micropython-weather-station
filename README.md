# Weather Station for my Greenhouse (WIP)

![Image Description](/images/device.jpg)

# Hardware needed

- [ESP32](https://botland.store/1322-esp32-wifi-and-bt-modules) based development board.
- [BME280](https://botland.store/pressure-sensors/11803-bme280-humidity-temperature-and-pressure-5904422366179.html) sensor.
- Power supply, Powerbank (without low current shutoff), or something else to power your device.
- Cables to connect things together.

# How to run code from this repository

1. Install [Micropython](https://micropython.org/download/ESP32_GENERIC/) on your ESP32 development board.
2. Connect BME280 sensor to proper Pins.
3. Upload all Python's `.py` files from this repository to your device (using [Thonny](https://thonny.org/) or [MPY-Jama](https://github.com/jczic/ESP32-MPY-Jama/releases)).
4. Configure device ([read below](https://github.com/Avaray/esp32-bme280-micropython-weather-station?tab=readme-ov-file#configuring-device)).
5. Reboot device and check terminal. Device will print messages on every important step (when booting, connecting to network, reading sensor, sending data, going to deep sleep).

# Configuring device

You need to change following settings in `config.py` file.

```python
# List of Wi-Fi networks
NETWORKS = [
  {"ssid": "My-Awesome-Network-Name", "password": "neverGuess123"}
]

# List of servers (URL's to upload sensor readings; names are optional)
SERVERS = [
  {"name": "primary", "url": "https://my.website.com"},
  {"name": "local", "url": "http://192.168.0.20:4000"},
]

# SCL and SDA pins for BME280 sensor
BME280_SCL_PIN = 22
BME280_SDA_PIN = 21
```

# The Server

I have written server code in [Typescript](https://www.typescriptlang.org/) for [Bun.js](https://bun.sh/). For the database, I'm using [MongoDB](https://www.mongodb.com/). The code is created for my needs and it's located in different repository. I need to modify it before sharing.

# TODO's

**In the first place**

- Do better Wi-Fi connection handling

**Later**

- Do better keyboard interruptions. To have the ability to stop the program at any time. Currently, I have programmed it to work, but it can be done better. I need to think about it.
- Better logging and add the option to disable logging to save energy (does it make sense?).
- User Interface for Access Point mode. The user should have the ability to configure the device through a browser. This feature is to be implemented last as it is of low priority.
- Check if BME280 library will work with BMP280
- Add ability to download latest files after boot
