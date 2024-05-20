# Weather Station for my Greenhouse (WIP)

![Image Description](/images/device.jpg)

# Hardware needed

- [ESP32](https://botland.store/1322-esp32-wifi-and-bt-modules) based development board.
- [BME280](https://botland.store/pressure-sensors/11803-bme280-humidity-temperature-and-pressure-5904422366179.html) or [BMP280](https://botland.store/pressure-sensors/7245-bmp280-digital-barometer-pressure-sensor-110kpa-i2cspi-33v-5904422310042.html) sensor.
- Power supply, Powerbank (without low current shutoff), or something else to power your device.
- Cables to connect things together.
- **(optional)** Jumper/Switch/Button.

# How to run code from this repository

1. Install [Micropython](https://micropython.org/download/ESP32_GENERIC/) on your ESP32 development board.
2. Connect BME280 sensor to proper Pins.
3. Modify configuration file ([read below](https://github.com/Avaray/esp32-bme280-micropython-weather-station?tab=readme-ov-file#configuring-device)).
4. Upload all Python's `.py` files to your device (using [Thonny](https://thonny.org/) or [MPY-Jama](https://github.com/jczic/ESP32-MPY-Jama/releases)).
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

# Admin Mode

**Admin Mode** creates an open network on the device. After connecting to the network, you can manage the device in a graphical interface. **Admin Mode** is mainly used to configure and debug the device.

By default, you must have **GPIO 16** and **GPIO 17** connected (shorted with [Jumper](<https://en.wikipedia.org/wiki/Jumper_(computing)>) for example) to start device in **Normal Mode**. Without this connection device will boot in **Admin Mode**. However, you can change the `ADMIN_MODE_REVERSED` variable in configuration file to `True`. After making this change, you will need to connect the mentioned pins to boot in **Admin Mode**.
You can also specify in the configuration file which pins should be used for **Admin Mode**.

_I'm thinking about completely reversing this method. This will most likely be changed soon._

# The Server

I have written server code in [Typescript](https://www.typescriptlang.org/) for [Bun.js](https://bun.sh/). For the database, I'm using [MongoDB](https://www.mongodb.com/). The code is created for my needs and it's located in different repository. I need to modify it before sharing.

# TODO's

**In the first place**

- Do better Wi-Fi connection handling

**Later**

- Do better keyboard interruptions. To have the ability to stop the program at any time. Currently, I have programmed it to work, but it can be done better. I need to think about it.
- Better logging and add the option to disable logging to save energy (does it make sense?).
- Web UI
- OTA updates
