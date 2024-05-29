# Official Micropython modules
from machine import SoftI2C, Pin

# Modules from the project
import config
import utils
import BME280

# Initialize I2C bus
i2c = SoftI2C(scl=Pin(config.SENSOR_SCL_PIN), sda=Pin(config.SENSOR_SDA_PIN))

# Initialize BME280 sensor
sensor = BME280.BME280(i2c)

def isValid(value):
  return value is not None and value != 0

def read():
  print('\nREADING DATA FROM SENSOR\n')
  sensor.read()
  data = {}
  if isValid(sensor.temperature):
    data['temperature'] = utils.normalizeNumber(sensor.temperature)
  if isValid(sensor.pressure):
    data['pressure'] = utils.normalizeNumber(sensor.pressure)
  if isValid(sensor.humidity):
    data['humidity'] = utils.normalizeNumber(sensor.humidity)
  return data
