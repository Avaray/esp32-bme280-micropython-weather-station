import network
import time
import urequests

import config

# Connect to Wi-Fi network
def connect():
  print('\nSTARTING WIFI\n')
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  networks = wlan.scan()
  print("Found", len(networks), "available networks")
  for knownNetwork in config.knownNetworks:
    ssid = knownNetwork["ssid"]
    password = knownNetwork["password"]
    if ssid in [network[0].decode() for network in networks]:
      print("Connecting to network", ssid)
      wlan.connect(ssid, password)
      timeout = time.time() + 15  # Set timeout to 15 seconds
      while not wlan.isconnected():
        if time.time() > timeout:
          print("Connection timeout")
          return False
        pass
      print("Connected to network", ssid)
      print("Network config:", wlan.ifconfig())

def send(data):
  print('\nSENDING DATA TO SERVER\n')
  print(data)
