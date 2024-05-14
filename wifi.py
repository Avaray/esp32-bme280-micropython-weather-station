print('\nSTARTING WIFI\n')

import machine
import network
import time

import config

# program logic: 
# 1. scan for wifi networks and connect to one that is specified in config.py 
# 2. if connection fails, try next network in the list
# 3. if all networks fail, go hibernate for 1 minute and try again
# 4. if connection is successful - print network name and IP address
# 5. read data from BME280 sensor
# 6. print temperature, pressure, and humidity
# 7. disconnect from wifi, go hibernate for 1 minute and repeat

# Connect to Wi-Fi network
def connect_to_wifi():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  networks = wlan.scan()
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
      return True
  return False

# Main loop
try:
    while True:
        if connect_to_wifi():
            # Read data from BME280 sensor
            print("Reading data from BME280 sensor...")
            print("Going to deep sleep for 1 minute...")
            #machine.deepsleep(60000)
            time.sleep(60)
        else:
            print("All known networks failed. Going to deep sleep for 1 minute...")
            #machine.deepsleep(60000)
            time.sleep(60)
            # throw exception to parent file
            raise Exception("All known networks failed")
except KeyboardInterrupt:
    print("Execution stopped by keyboard interrupt")
