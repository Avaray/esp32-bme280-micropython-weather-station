print('\nBOOTING DEVICE\n')

# Official micropython modules
import machine
import time

# Check if the device was woken from a deep sleep or hard reset and print proper message
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
  print('Woke from a deep sleep')
else:
  print('Booting after a hard reset or power on')

print('Press Ctrl-C to interrupt boot and start a REPL session\n')
# Wait 5 seconds for user to interrupt the boot process 
# This part doesn't work well. Need to fix it / or find a better way to keyboard interrupt in the boot process
# Currently when you press Ctrl-C, message "Interrupted by keyboard (Ctrl-C)" is printed, but the code execution continues
try:
  for i in range(5, 0, -1):
    print(i, end='...')
    time.sleep(1)
except KeyboardInterrupt:
  print('\nInterrupted by keyboard (Ctrl-C)\n')
else:
  print('0')

# Start the main code
# I wan't to avoid using the main.py file, because main.py is executed every time the device boots, and I don't like that
# I want to be able to interrupt the boot process and start a REPL session before the main code starts
import index
