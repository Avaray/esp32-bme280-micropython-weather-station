print('\nSTARTING MAIN\n')

import esp
import sys
import machine

import config
import helpers

if machine.reset_cause() != machine.DEEPSLEEP_RESET:
  print('Device name:', config.deviceName.upper())
  print('Platform:', sys.platform.upper())
  print('Flash size:', esp.flash_size() // 1024 // 1024, 'MB')
  print('Micropython Firmware Version', helpers.tupleToSemver(sys.implementation.version))
  print('Python version', helpers.tupleToSemver(sys.version_info))
  print('CPU frequency:', machine.freq(), 'Hz')

  if not config.knownNetworks:
    print('No known networks found in config.py')
    print('Please add at least one network to networks list')
    sys.exit()
  else:
    print('Known Wi-Fi networks:', len(config.knownNetworks))

  # Set CPU frequency to 80MHz (default is 160MHz) to save power
  if machine.freq() != 80000000:
    print('Setting CPU frequency to 80MHz')
    machine.freq(80000000)

# connect to wifi (code is in wifi.py)
# use try catch block to handle exceptions
try:
  import wifi
except Exception as e:
  print(f"An error occurred when importing wifi.py: {e}")

# if wifi connection is successful, read data from BME280 sensor (code is in sensor.py)
# use try catch block to handle exceptions
try:
  import readsensor
except Exception as e:
  print(f"An error occurred when importing sensor.py: {e}")

# go to deep sleep for 10 seconds
print('Going to deep sleep for 5 seconds...')
# machine.deepsleep(5000)

