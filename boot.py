import machine
import time

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')
else:
    print('\nBooting after a hard reset or power on')
    print('Press Ctrl-C to interrupt boot and start a REPL session\n')
    # wait 5 seconds for user to interrupt the boot process 
    try:
        for i in range(5, 0, -1):
            print(i, end='...')
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nInterrupted by keyboard (Ctrl-C)\n')
    else:
        print('0')
