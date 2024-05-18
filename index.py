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

  data['deviceName'] = config.deviceId

  if machine.reset_cause() != machine.DEEPSLEEP_RESET:
    print('Device name:', config.deviceId.upper())
    print('Platform:', sys.platform.upper())
    print('Flash size:', esp.flash_size() // 1024 // 1024, 'MB')
    print('Micropython Firmware Version', helpers.tupleToSemver(sys.implementation.version))
    print('Python version', helpers.tupleToSemver(sys.version_info))
    print('CPU frequency:', machine.freq(), 'Hz')

    # check if any networks are defined in config file
    if not config.networks:
      print('No known networks found in config.py')
      print('Please add at least one network to networks list')
      sys.exit()
    else:
      print('Known Wi-Fi networks:', len(config.networks))

    # Set CPU frequency to 80MHz (default is 160MHz) to save power
    if machine.freq() != 80000000:
      print('Setting CPU frequency to 80MHz')
      machine.freq(80000000)

  # connect to the Wi-Fi network
  wifi.connect()

  # add sensor readings to the data dictionary
  data.update(sensor.read())

  print('Temperature:', data['temperature'], '°C')
  print('Pressure:', data['pressure'], 'hPa')
  print('Humidity:', data['humidity'], '%')

  data['esp32'] = helpers.normalizeNumber(helpers.fahrenheitToCelsius(esp32.raw_temperature()))

  print('Device temperature:', data['esp32'], '°C')

  # send data to the server
  for server in config.servers:
    url = server['url']
    try:
      wifi.send(url, data)
      print('Data sent successfully')
      break  # stop the loop when data is sent successfully
    except Exception as e:
      print('Failed to send data', str(e))

  # put the device to deep sleep for amount of minutes specified in config.py as frequency variable
  print('Going to deep sleep for', config.frequency, 'minutes')
  sleepTime = config.frequency * 60 * 1000
  machine.deepsleep(sleepTime)

except KeyboardInterrupt:
  print('KeyboardInterrupt detected. Exiting...')
