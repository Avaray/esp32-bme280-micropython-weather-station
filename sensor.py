# Official Micropython modules
from machine import SoftI2C, Pin

# Project files
from config import SENSOR_SCL_PIN, SENSOR_SDA_PIN
from utils import normalize_number
import BME280

# Initialize I2C bus
i2c = SoftI2C(scl=Pin(SENSOR_SCL_PIN), sda=Pin(SENSOR_SDA_PIN))

# Initialize BME280 sensor
sensor = BME280.BME280(i2c)

def isValid(value):
  return value is not None and value != 0

def read():
  print('\nREADING DATA FROM SENSOR\n')
  sensor.read()
  data = {}
  if isValid(sensor.temperature):
    data['temperature'] = normalize_number(sensor.temperature)
  if isValid(sensor.pressure):
    data['pressure'] = normalize_number(sensor.pressure)
  if isValid(sensor.humidity):
    data['humidity'] = normalize_number(sensor.humidity)
  return data
