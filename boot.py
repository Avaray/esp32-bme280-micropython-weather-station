# Official MicroPython modules
import machine
import time

# Project files
import config

output_pin = machine.Pin(config.ADMIN_MODE_PIN_OUT, machine.Pin.OUT)
input_pin = machine.Pin(config.ADMIN_MODE_PIN_IN, machine.Pin.IN)

output_pin.value(1)

admin_mode = (input_pin.value() == 0 and not config.ADMIN_MODE_REVERSED) or (input_pin.value() == 1 and config.ADMIN_MODE_REVERSED)

if admin_mode:
  print('\nBooting device in Admin Mode\n'.upper())
  import admin
else:
  if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('\nBooting device in Normal Mode after waking from deep sleep\n'.upper())
  else:
    print('\nBooting device in Normal Mode after hard reset or power on\n'.upper())

  print('Notice: Connect GPIO', config.ADMIN_MODE_PIN_OUT, 'and GPIO', config.ADMIN_MODE_PIN_IN, 'to boot in Admin Mode\n')
  import normal
