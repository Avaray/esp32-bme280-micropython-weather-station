# official micropython modules
from machine import SoftI2C, Pin
import BME280

# modules from the project
import config
import helpers

i2c = SoftI2C(scl=Pin(config.BME280_SCL_PIN), sda=Pin(config.BME280_SDA_PIN))
sensor = BME280.BME280(i2c)

def isValid(value):
  return value is not None and value != 0

def read():
  print('\nREADING DATA FROM SENSOR\n')
  sensor.read()
  data = {
    "temperature": helpers.normalizeNumber (sensor.temperature) if isValid(sensor.temperature) else 0,
    "pressure": helpers.normalizeNumber(sensor.pressure) if isValid(sensor.pressure) else 0,
    "humidity": helpers.normalizeNumber(sensor.humidity) if isValid(sensor.humidity) else 0
  }
  return data
