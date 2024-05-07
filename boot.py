import sys
import config # config.py file
import helpers # helpers.py file

print('\nSTARTING\n')
print('Device name:', config.DEVICE_NAME.upper())
print('Platform:', sys.platform.upper())
print('Micropython Firmware Version', helpers.tuple_to_semver(sys.implementation.version))
print('Python version', helpers.tuple_to_semver(sys.version_info))
