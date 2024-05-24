# Official Micropython modules
import os
import utime
import hashlib
import binascii
import urequests as req

# Modules from the project
import config

# Convert tuple to semver string
def tupleToSemver(tuple):
  return '.'.join(map(str, tuple)).strip('.').strip(',')

# Convert Fahrenheit to Celsius
def fahrenheitToCelsius(fahrenheit):
  return (fahrenheit - 32) * 5.0/9.0

# Normalize number to two decimal places
def normalizeNumber(number):
  number = float("{:.2f}".format(number))
  return number

# Get list of log files
def getLogsList(logsDir=config.LOGS_DIR):
  try:
    logs = os.listdir(logsDir)
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
