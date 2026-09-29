from gpiozero import Button
from signal import pause
import time

button_pin = 18 #GPIO2

def test_complete():
    print("Test complete")

button = Button(button_pin, pull_up=True)

# while True:
#     if button.is_pressed:
#         print("State 1")
#     else:
#         print("State 0")
#     time.sleep(1)

button.when_pressed=test_complete

print("Waiting for press...")    

pause()

print("Exiting...")