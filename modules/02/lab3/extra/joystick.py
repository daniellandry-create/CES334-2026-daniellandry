from gpiozero import Button
from signal import pause
import time

button_pin = 2 #GPIO2

def test_complete():
    print("Test complete")

switch = Button(button_pin, pull_up=True)

while True:
    if switch.is_pressed:
        print("State 1")
    else:
        print("State 0")
    time.sleep(1)

print("Waiting for press...")    

pause()

print("Exiting...")