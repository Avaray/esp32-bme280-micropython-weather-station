# Official Micropython modules
import os
import sys
import utime
import machine
import hashlib
import ubinascii as binascii
import urequests as req
import ujson as json

# Project files
import config

# Convert tuple to semver string
def tuple_to_semver(tuple):
  return '.'.join(map(str, tuple)).strip('.').strip(',')

# Check if the provided string is a valid semver
def is_valid_semver(semver):
  import re
  return bool(re.match(r'^\d+\.\d+(\.\d+)?$', semver))

# Check if Micropython version is 1.22 or higher
def is_micro_python_version_sufficient(current, required='1.22.0'):
  print('Checking Micropython version')

  if not is_valid_semver(current) or not is_valid_semver(required):
    print('One of the provided versions is not a valid semver string')
    return False

  current = tuple(map(int, current.split('.')))
  required = tuple(map(int, required.split('.')))
  if current >= required:
    return True
  else:
    print('Micropython version', tuple_to_semver(current), 'is not sufficient, required version is', tuple_to_semver(required))
    return False

# Convert Fahrenheit to Celsius
def fahrenheit_to_celsius(fahrenheit):
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

# Get list of all project files
# TODO: Auto detect project structure
def project_files_list():
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

# Read data from a file
def read_file(filename, directory='/'):
  try:
    with open(directory + filename, 'r') as file:
      return file.read()
  except Exception as e:
    print('Failed to read log', str(e))
    return None

# Save data a file (overwrites the file if it exists)
def save_file(filename, directory='/', data):
  try:
    with open(directory + filename, 'w') as file:
      file.write(data)
  except Exception as e:
    print('Failed to save file', str(e))

# Delete single file
def delete_file(directory='/', filename):
  try:
    os.remove(directory + filename)
  except Exception as e:
    print('Failed to delete file', str(e))

# If the number of logs exceeds the limit, the oldest logs are deleted
def delete_old_logs(logs_dir=config.LOGS_DIR, maxFiles=config.LOGS_MAX_FILES):
  try:
    logs = os.listdir(logs_dir)
    logs.sort(key=lambda x: os.stat(logs_dir + x).st_mtime)
    while len(logs) > maxFiles:
      os.remove(logs_dir + logs[0])
      logs.pop(0)
  except Exception as e:
    print('Failed to delete old logs', str(e))

# Download file from the server
def download_file(url, file_path):
  try:
    response = req.get(url)
    with open(file_path, 'wb') as file:
      file.write(response.content)
    return True
  except Exception as e:
    print('Failed to download file', str(e))
    return False

# Get file content MD5 hash
# This function will be used for OTA updates
def md5_file_content_hash(file_path):
  hash_md5 = hashlib.md5()
  with open(file_path, "rb") as f:
      for line in f:
          hash_md5.update(line)
  return binascii.hexlify(hash_md5.digest()).decode()

# Send data to the server
def send_data(url, data):
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
def able_to_boot(able=True):

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
  if not is_micro_python_version_sufficient(micropython_version):
    print('Micropython version', micropython_version, 'is not sufficient, required version is 1.22.0 or higher')
    able = False

  return able

# Get unique machine ID
def machine_unique_id():
  binary = machine.unique_id()
  decoded = binascii.hexlify(binary).decode('utf-8')
  return decoded