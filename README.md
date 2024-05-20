# Weather Station for my Greenhouse (WIP)

![Image Description](/images/device.jpg)

# Required Hardware

- [ESP32](https://botland.store/1322-esp32-wifi-and-bt-modules) based development board.
- [BME280](https://botland.store/pressure-sensors/11803-bme280-humidity-temperature-and-pressure-5904422366179.html) or [BMP280](https://botland.store/pressure-sensors/7245-bmp280-digital-barometer-pressure-sensor-110kpa-i2cspi-33v-5904422310042.html) sensor.
- Power supply, Powerbank (without low current shutoff), or something else to power your device.
- Cables to connect things together.

# How to run code from this repository

1. Install [Micropython](https://micropython.org/download/ESP32_GENERIC/) on your ESP32 development board.
2. Connect BME280 or BMP280 sensor to proper Pins.
3. Modify `config.py` configuration file.
4. Upload all Python's `.py` files to your device (using [Thonny](https://thonny.org/) or [MPY-Jama](https://github.com/jczic/ESP32-MPY-Jama/releases)).
5. Reboot device and check terminal. Device will print messages on every important step (when booting, connecting to network, reading sensor, sending data, going to deep sleep).

# Configuring device

You need to change following settings in `config.py` file.  
Below you see only the most important settings. You will find more inside the file.

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

# SCL and SDA pins for the sensor
SENSOR_SCL_PIN = 22
SENSOR_SDA_PIN = 21
```

# Admin Mode

**Admin Mode** creates an open network on the device. After connecting to the network, you can manage the device in a graphical interface. **Admin Mode** is mainly used to configure and debug the device.

To start device in **Admin Mode** you must have **GPIO 16** and **GPIO 17** pins connected (shorted with [Jumper](<https://en.wikipedia.org/wiki/Jumper_(computing)>) for example). Without this connection device will boot in **Normal Mode**.

However, you can change the `ADMIN_MODE_REVERSED` variable in configuration file to `True`. After making this change, you will need to connect the mentioned pins to boot in **Normal Mode**. Booting without connected pins will start the device in **Admin Mode**.

You can also specify in the configuration file which pins should be used for **Admin Mode**.

# The Server

You can create your own server to receive data from the device. The server must be able to receive [POST requests](<https://en.wikipedia.org/wiki/POST_(HTTP)>) with [JSON](https://en.wikipedia.org/wiki/JSON) data. You can use any backend technology you want. If you will use Python for serverm, you can easily convert JSON data to a dictionary using `json.loads()` function.

Device sends JSON data to specified in configuration file [URL's](https://en.wikipedia.org/wiki/URL).  
Below you can see an example of the data sent by the device.

```json
{
  "temperature": 21.5,
  "humidity": 50.0,
  "pressure": 1013.25
}
```

If you use BMP280 sensor, the humidity value will be `0`.  
That's because BMP280 sensor does not measure humidity.

### My server code

I have written my own server code in [Typescript](https://www.typescriptlang.org/) for [Bun.js](https://bun.sh/). The code is created for my needs and I need to modify it before making it public.
Currently I spend my time on the device code, but I will publish the server code in the future.

# TODO's

**In the first place**

- Do better Wi-Fi connection handling

**Later**

- Do better keyboard interruptions. To have the ability to stop the program at any time. Currently, I have programmed it to work, but it can be done better. I need to think about it.
- Better logging and add the option to disable logging to save energy (does it make sense?).
- Web UI
- OTA updates, plus code backup
