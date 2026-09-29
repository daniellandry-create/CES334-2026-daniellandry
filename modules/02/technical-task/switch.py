from gpiozero import Button
from signal import pause
import time

switch_pin = 17 #GPIO2

def test_complete():
    print("Test complete")

switch = Button(switch_pin, pull_up=True)

while True:
    if switch.is_pressed:
        print("State 1")
    else:
        print("State 0")
    time.sleep(1)

print("Waiting for press...")    

pause()

print("Exiting...")