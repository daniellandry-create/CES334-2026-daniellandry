from gpiozero import Button
from signal import pause
import time
from functools import partial


strings = ["\x1b[35mFizz\x1b[30m", "\x1b[36mBuzz\x1b[30m", "\x1b[37mFizzBuzz\x1b[30m", "\x1b[33mLightyear\x1b[30m"]


input_mode = False
output_mode = 0


button_pin = 22 #GPIO22
switch_pin = 23 #GPIO23
joystick_pin = 24 #GPIO24


button = Button(button_pin, bounce_time=0.05)
switch = Button(switch_pin, bounce_time=0.05)
joystick = Button(joystick_pin, bounce_time=0.05)


class State:
   def __init__(self):
       self.output_mode=0


state=State()


#Output
def action():
   if switch.is_pressed:
       print("\x1b[31mNot in display mode... flip the switch!\x1b[30m")
   else:
       print(strings[state.output_mode])


# Flick Joystick in positive x-direction to change output_mode
def change_output_mode(state):
   if switch.is_pressed:
       state.output_mode = (state.output_mode + 1) % 4
       print(f"\x1b[34mNow writing: {strings[state.output_mode]}\x1b[30m")
   else:
       print("\x1b[31mNot in selection mode... flip the switch!\x1b[30m")


def enter_selection_mode():
   print("\x1b[32mEntering selection mode...\x1b[30m")


def exit_selection_mode():
   print("\x1b[32mExiting selection mode...\x1b[30m")


output_mode_ptr = partial(change_output_mode, state)


button.when_pressed=action
joystick.when_pressed=output_mode_ptr
switch.when_pressed=enter_selection_mode
switch.when_released=exit_selection_mode


if switch.is_pressed:
   print("\x1b[32mHello! You are in selection mode\x1b[30m")
else:
   print("\x1b[32mHello! You are in display mode\x1b[30m")


pause()
