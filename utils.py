import config

# Convert tuple to semver string
def tupleToSemver(version_tuple):
  return '.'.join(map(str, version_tuple)).strip('.').strip(',')

# Convert Fahrenheit to Celsius
def fahrenheitToCelsius(fahrenheit):
  return (fahrenheit - 32) * 5.0/9.0

# Normalize number to two decimal places
def normalizeNumber(number):
  number = float("{:.2f}".format(number))
  return number

# If the number of logs exceeds the limit, the oldest logs are deleted
def deleteOldLogs(logsDir=config.LOGS_DIR, maxFiles=config.LOGS_MAX_FILES):
  import os
  try:
    logs = os.listdir(logsDir)
    logs.sort(key=lambda x: os.stat(logsDir + x).st_mtime)
    while len(logs) > maxFiles:
      os.remove(logsDir + logs[0])
      logs.pop(0)
  except Exception as e:
    print('Failed to delete old logs', str(e))

# Save logs to a file (overwrites the file if it exists)
def saveLog(filename, logsDir=config.LOGS_DIR, data):
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