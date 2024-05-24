print('Admin (WIP)')

# Official micropython modules
import network
import uasyncio as asyncio

# Modules from the project
import config

# Start the Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)

# Set the AP configuration
ssid = config.AP_SSID if isinstance(config.AP_SSID, str) and config.AP_SSID else 'Weather Station'
password = config.AP_PASSWORD if isinstance(config.AP_PASSWORD, str) and config.AP_PASSWORD else None
authmode = network.AUTH_WPA_WPA2_PSK if password else network.AUTH_OPEN
ap.config(ssid=ssid, authmode=authmode, password=password)

print('AP started:', ap.ifconfig())

