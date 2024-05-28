# Official micropython modules
import esp
import esp32
import sys
import machine

# Modules from the project
import config
import utils
import sensor
from wifi import connect

# Everything is enclosed in try-catch block to catch KeyboardInterrupt
# I'm still looking for a better way to interrupt code execution to be able to edit files in IDE
try:
  # Initialize data dictionary that will be sent to the server
  data = {}

  # Add device name to the data dictionary
  if config.DEVICE_ID:
    data['device_id'] = config.DEVICE_ID
  
  # Print device information if the device was not woken from deep sleep
  if machine.reset_cause() != machine.DEEPSLEEP_RESET:

    if config.DEVICE_ID:
      print('Device ID:', config.DEVICE_ID.upper())
    else:
      print('Device ID is not specified')

    print('Platform:', sys.platform.upper())
    print('Flash size:', esp.flash_size() // 1024 // 1024, 'MB')
    print('Micropython Firmware Version', utils.tupleToSemver(sys.implementation.version))
    print('Python version', utils.tupleToSemver(sys.version_info))
    print('CPU frequency:', machine.freq(), 'Hz')

    # Check if any networks are defined in config file
    if not config.NETWORKS:
      print('No known networks found in config.py')
      print('Please add at least one network to networks list')
      sys.exit()
    else:
      print('Known Wi-Fi networks:', len(config.NETWORKS))

    # Set CPU frequency to 80MHz (default is 160MHz) to save power
    if machine.freq() != 80000000:
      print('Setting CPU frequency to 80MHz')
      machine.freq(80000000)

  # Connect to the Wi-Fi network
  connect()

  # Add sensor readings to the data dictionary
  data.update(sensor.read())

  print('Temperature:', data['temperature'], '°C')
  print('Pressure:', data['pressure'], 'hPa')
  print('Humidity:', data['humidity'], '%')

  data['esp32'] = utils.normalizeNumber(utils.fahrenheitToCelsius(esp32.raw_temperature()))

  print('Device temperature:', data['esp32'], '°C')

  # Send data to the server
  for server in config.SERVERS:
    url = server['url']
    try:
      utils.send(url, data)
      print('Data sent successfully')
      break
    except Exception as e:
      print('Failed to send data', str(e))

  # put the device to deep sleep for amount of minutes specified in config.py as frequency variable
  print('Going to deep sleep for', config.FREQUENCY, 'minutes')
  sleepTime = config.FREQUENCY * 60 * 1000
  machine.deepsleep(sleepTime)

except KeyboardInterrupt:
  print('KeyboardInterrupt detected. Exiting...')
