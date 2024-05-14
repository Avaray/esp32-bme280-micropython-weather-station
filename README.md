# Small project for my Greenhouse

...

# Hardware needed

- ESP32 based development board
- BME280 sensor

# Preparations

...

# How to run

...

# Configuring device

You need to upload `config.py` file to your device.

```python
# Name for your device (optional)
deviceName = ""

# List of Wi-Fi networks
knownNetworks = [
  {"ssid": "", "password": ""}
]

# Server address
serverUrl = "https://example.com:8000"

# How often check readings and send them to server (in minutes)
frequency = 10
```
