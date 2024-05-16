import network
import time
import urequests as req
import ujson as json

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
  print('\nSENDING READINGS TO SERVER\n')
  try:
    headers = {'Content-Type': 'application/json'}
    res = req.post(config.serverUrl, headers=headers, json=json.dumps(data))
    res.close()
    # check if the server responded with status code 200
    if res.status_code == 200:
      print('Successfully sent data to server')
      return True
    # check if the server responded with any status code
    elif res.status_code and isinstance(res.status_code, int):
      print('Received status code:', res.status_code)
      return False
    # if the server didn't respond with status code
    else:
      print('No status code received')
      return False

  except OSError as e:
    print('OSError:', e)
    return False
