import sys
import machine

try:
    import config
except ImportError:
    print('Error: config.py not found.')
    sys.exit()

try:
    import helpers
except ImportError:
    print('Error: helpers.py not found.')
    sys.exit()

print('\nSTARTING\n')
print('Device name:', config.deviceName.upper())
print('Platform:', sys.platform.upper())
print('Micropython Firmware Version', helpers.tupleToSemver(sys.implementation.version))
print('Python version', helpers.tupleToSemver(sys.version_info))
print('CPU frequency:', machine.freq(), 'Hz')

if not config.knownNetworks:
    print('No known networks found in config.py')
    print('Please add at least one network to knownNetworks list')
    sys.exit()
else:
    print('Known networks:', len(config.knownNetworks))

# Set CPU frequency to 80MHz (default is 160MHz) to save power
print('Setting CPU frequency to 80MHz')
machine.freq(80000000)
