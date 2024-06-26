# Weather Station for my Greenhouse (WIP)

![Image Description](/images/device.jpg)

# Required Hardware

- [ESP32](https://botland.store/1322-esp32-wifi-and-bt-modules) based development board.
- [BME280](https://botland.store/pressure-sensors/11803-bme280-humidity-temperature-and-pressure-5904422366179.html) or [BMP280](https://botland.store/pressure-sensors/7245-bmp280-digital-barometer-pressure-sensor-110kpa-i2cspi-33v-5904422310042.html) sensor.
- Power supply, Powerbank (without low current shutoff), or something else to power your device.
- Cables to connect things together.

# How to run code from this repository

1. Install [Micropython](https://micropython.org/download/ESP32_GENERIC/) (1.13+) on your ESP32 development board.
2. Connect BME280 or BMP280 sensor to proper Pins.
3. Modify `config.py` configuration file.
4. Upload all Python's `.py` files to your device (using [Thonny](https://thonny.org/) or [MPY-Jama](https://github.com/jczic/ESP32-MPY-Jama/releases)).
5. Reboot device and check terminal. Device will print messages on every important step (when booting, connecting to network, reading sensor, sending data, going to deep sleep).

# Configuring device

You can configure your device by editing the `config.py` file.  
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

# Admin Mode (Work in Progress)

`UI not included yet`
`Code not fully implemented yet`

**Admin Mode** creates an open network on the device. After connecting to the network, you can manage the device in a graphical interface. **Admin Mode** is mainly used to configure and debug the device.

To start device in **Admin Mode** you must have **GPIO 16** and **GPIO 17** pins connected (shorted with [Jumper](<https://en.wikipedia.org/wiki/Jumper_(computing)>) for example). Without this connection device will boot in **Normal Mode**.

However, you can change the `ADMIN_MODE_REVERSED` variable in configuration file to `True`. After making this change, you will need to connect the mentioned pins to boot in **Normal Mode**. Booting without connected pins will start the device in **Admin Mode**.

You can also specify in the configuration file which pins should be used for **Admin Mode**.

# The Server

You can create your own server to receive data from the device. The server must be able to receive [POST requests](<https://en.wikipedia.org/wiki/POST_(HTTP)>) with [JSON](https://en.wikipedia.org/wiki/JSON) data. You can use any backend technology you want. If you will use Python for server, you can easily convert JSON data to a dictionary using `json.loads()` function.

Device sends JSON data to specified in configuration file [URL's](https://en.wikipedia.org/wiki/URL).  
Below you can see an example of the data sent by the device.

```json
{
  "temperature": 21.5,
  "humidity": 50.0,
  "pressure": 1013.25
}
```

The device will send only the readings that are available. If the device does not have the ability to measure something, it will not be included in the JSON data.

## Example of server code ([BUN.js](https://bun.sh/))

Following code is based on [this example](https://bun.sh/guides/http/server) from official documentation.

```javascript
const server = Bun.serve({
  async fetch(req) {
    if (req.method === 'POST') {
      const data = await req.json();
      console.log('Received readings:', data);
      return Response.json({ status: 200 });
    }
    return new Response('Page not found', { status: 404 });
  },
});
console.log(`Listening on ${server.url}`);
```

# TODO's

**Currently working on**

- Admin Mode + Web UI
- In Admin Mode, force connected client to open a browser with the device's IP address (Captive Portal).
- Scan for available Wi-Fi networks and display them in Admin Mode.

**In the first place**

- Do better Wi-Fi connection handling

**Later**

- Do better keyboard interruptions. To have the ability to stop the program execution at any time (except when sleeping, ofc.). Currently, I have programmed it to work, but it can be done better. I need to think about it.
- Better logging and add the option to disable logging to save energy (does it make sense?).
- OTA updates, Pre-commit hook to generate hashes for all files, plus code backup (to prevent bricking the device)
- Custom `machine.wake_reason()` for reboots to Admin Mode. If config is not correct, the device will reboot to Admin Mode.

# Notes

[Camelcase](https://developer.mozilla.org/en-US/docs/Glossary/Camel_case) is used in the code because I came from the JavaScript world. I know that in Python, the convention is to use [snake_case](https://developer.mozilla.org/en-US/docs/Glossary/Snake_case). Formatting in Python is also crazy for me, but I'm working on both of these things. I'm trying to find a good formatter.
