print('\nSTARTING MAIN\n')

import esp
import esp32
import sys
import machine

import config
import wifi
import sensor
import helpers

data = {}

data['deviceName'] = config.deviceName

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

wifi.connect()

# add sensor.read() to data
data.update(sensor.read())

print('Temperature:', data['temperature'], '°C')
print('Pressure:', data['pressure'], 'hPa')
print('Humidity:', data['humidity'], '%')

# include ESP32 temperature
data['esp32'] = helpers.normalizeNumber(helpers.fahrenheitToCelsius(esp32.raw_temperature()))

print('Device temperature:', data['esp32'], '°C')

# send data to server
send(data)

# print('Going to deep sleep for 5 seconds...')
# machine.deepsleep(5000)
