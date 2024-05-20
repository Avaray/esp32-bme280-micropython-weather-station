# Official Micropython modules
import os

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

# OTA update
# todo...
