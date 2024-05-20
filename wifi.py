# official micropython modules
import network
import time
import urequests as req
import ujson as json

# modules from the project
import config

# Connect to Wi-Fi network
def connect():
  print('\nSTARTING WIFI\n')

  # Check if the device is already connected to the network
  if network.WLAN(network.STA_IF).isconnected():
    print('Already connected to the network')
    return True
  else:
    print('Not connected to the network')

    # Create an instance of the WLAN class
    wlan = network.WLAN(network.STA_IF)

    if config.DEVICE_ID:        
      # Check if the network hostname is already set to the device ID
      if network.hostname() == config.DEVICE_ID:
        print('Proper network hostname already set', network.hostname())
      # if not, set it to the device ID
      else:
        print('Changing network hostname from', network.hostname(), 'to', config.DEVICE_ID)
        # wlan.config(hostname=config.DEVICE_ID) # I think it's deprecated
        network.hostname(config.DEVICE_ID)

    # Activate the Wi-Fi interface
    wlan.active(True)
    # Scan for available networks
    networks = wlan.scan()
    # Print the number of available networks
    print("Found", len(networks), "available networks")

    # Check if any of the networks is available
    for knownNetwork in config.NETWORKS:
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
        print("Assigned IP address:", wlan.ifconfig()[0])

    # let's print MAC address of the device (this must be removed in future, because it consumes power and is not needed)
    MAC = ':'.join(f'{b:02X}' for b in wlan.config('mac'))
    print('MAC address:', MAC)

# Send data to the server
def send(url, data):
  print('\nSENDING READINGS TO SERVER\n')

  print('Sending data to', url)
  try:
    headers = {'Content-Type': 'application/json'}
    res = req.post(url, headers=headers, json=json.dumps(data))
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
