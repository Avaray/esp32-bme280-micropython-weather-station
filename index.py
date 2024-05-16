import esp
import esp32
import sys
import machine
import config
import helpers
import wifi
import sensor

print('\nSTARTING MAIN\n')

try:
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

  data.update(sensor.read())

  print('Temperature:', data['temperature'], '°C')
  print('Pressure:', data['pressure'], 'hPa')
  print('Humidity:', data['humidity'], '%')

  data['esp32'] = helpers.normalizeNumber(helpers.fahrenheitToCelsius(esp32.raw_temperature()))

  print('Device temperature:', data['esp32'], '°C')

  # send data to server. try 10 times before giving up
  for i in range(1, 4):
    if wifi.send(data):
      break
    else:
      print('Failed to send data to server. Retrying', i, 'of 3')
      continue
  

  # put the device to deep sleep for amount of minutes specified in config.py as frequency variable
  print('Going to deep sleep for', config.frequency, 'minutes')
  sleepTime = config.frequency * 60 * 1000
  machine.deepsleep(sleepTime)

except KeyboardInterrupt:
  print('KeyboardInterrupt detected. Exiting...')
