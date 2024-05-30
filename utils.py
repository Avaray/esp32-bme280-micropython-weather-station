# Official Micropython modules
import os
import sys
import utime
import hashlib
import binascii
import urequests as req
import ujson as json

# Modules from the project
import config

# Convert tuple to semver string
def tuple_to_semver(tuple):
  return '.'.join(map(str, tuple)).strip('.').strip(',')

# Check if Micropython version is 1.22 or higher
def isMicropythonVersionSufficient(current, required='1.22.0'):

  print('Checking Micropython version')

  import re
  if not re.match(r'^\d+\.\d+(\.\d+)?$', current):
    print('Provided version is not in semver format, expected format is x.y.z')
    return False

  current = tuple(map(int, current.split('.')))
  required = tuple(map(int, required.split('.')))
  if current >= required:
    return True
  else:
    print('Micropython version', tuple_to_semver(current), 'is not sufficient, required version is', tuple_to_semver(required))
    return False

# Convert Fahrenheit to Celsius
def fahrenheitToCelsius(fahrenheit):
  return (fahrenheit - 32) * 5.0/9.0

# Normalize number to two decimal places
def normalize_number(number):
  number = float("{:.2f}".format(number))
  return number

# Get list of log files
def get_log_list(logs_dir=config.LOGS_DIR):
  try:
    logs = os.listdir(logs_dir)
    return logs
  except Exception as e:
    print('Failed to get logs list', str(e))
    return None

# Get list of all .py files in the project
def getProjectFilesList():
  try:
    files = {
      'python': [],
      'web': []
    }
    pythonFiles = os.listdir('/')
    pythonFiles = [file for file in pythonFiles if file.endswith('.py')]
    webFiles = []
    if 'web' in os.listdir('/'):
      webFiles = os.listdir('/web')
    files['python'] = pythonFiles
    files['web'] = webFiles
    return files
  except Exception as e:
    print('Failed to get project files list', str(e))
    return None

# Delete single log file
def deleteLog(filename, logsDir=config.LOGS_DIR):
  try:
    os.remove(logsDir + filename)
  except Exception as e:
    print('Failed to delete log', str(e))

# If the number of logs exceeds the limit, the oldest logs are deleted
def deleteOldLogs(logsDir=config.LOGS_DIR, maxFiles=config.LOGS_MAX_FILES):
  try:
    logs = os.listdir(logsDir)
    logs.sort(key=lambda x: os.stat(logsDir + x).st_mtime)
    while len(logs) > maxFiles:
      os.remove(logsDir + logs[0])
      logs.pop(0)
  except Exception as e:
    print('Failed to delete old logs', str(e))

# Save logs to a file (overwrites the file if it exists)
def saveLog(filename, data, logsDir=config.LOGS_DIR):
  try:
    with open(logsDir + filename, 'w') as file:
      file.write(data)
  except Exception as e:
    print('Failed to save log', str(e))

# Read logs from a file
def readLog(filename, logsDir=config.LOGS_DIR):
  try:
    with open(logsDir + filename, 'r') as file:
      return file.read()
  except Exception as e:
    print('Failed to read log', str(e))
    return None

# Get file content MD5 hash
def md5FileContentHash(file_path):
  hash_md5 = hashlib.md5()
  with open(file_path, "rb") as f:
      for line in f:
          hash_md5.update(line)
  return binascii.hexlify(hash_md5.digest()).decode()

# Download file from the server
def downloadFile(url, file_path):
  try:
    response = req.get(url)
    with open(file_path, 'wb') as file:
      file.write(response.content)
    return True
  except Exception as e:
    print('Failed to download file', str(e))
    return False

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

  except Exception as e:
    print('Failed to send data to server', str(e))
    return False

# Validate required things before booting
def ableToBoot(able=True):

  if not config.NETWORKS:
    print('No networks defined in config file')
    able = False

  for network in config.NETWORKS:
    if not network['ssid']:
      print('Network SSID cannot be empty')
      able = False

  if not config.SERVERS:
    print('No servers defined in config file')
    able = False
    
  for server in config.SERVERS:
    if not server['url']:
      print('Server URL cannot be empty')
      able = False

  # Check if Micropython version is sufficient
  micropython_version = tuple_to_semver(sys.implementation.version)
  if not isMicropythonVersionSufficient(micropython_version):
    print('Micropython version', micropython_version, 'is not sufficient, required version is 1.22.0 or higher')
    able = False

  return able
