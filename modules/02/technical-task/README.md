# Creative Embedded Systems

## Lab 3 - Hands-on Hardware

Performed by: Ryan Fernandes and Daniel Landry

**Lab Video:** [Watch on YouTube](https://youtu.be/yrpZpNRvjTg)

### Action Plan

1. Research how to use Python to interact with GPIO pins
2. Do 3 sample scripts and circuits to read **debounced** input from all 3 components
3. Combine all 3 sample scripts and circuit and display the state of all 3 components at the same time
4. Program the 5 "modes"

### Execution

1. Research how to use Python to interact with GPIO pins
    
    - There is gpiozero and RPi.GPIO
    - gpiozero wraps RPi.GPIO and is installed by default on Raspberry Pi OS
    - We will start by using gpiozero

2. Do 3 sample scripts and circuits to read **debounced** input from all 3 components

    - Switch can be implemented using Button
    - gpiozero uses the same pinout as the raspberry pi has
    - pause() causes the process to sleep until a signal is received, then the appropriate handler will be called
    - Button() in GPIO zero to do a button or a switch
        - pull_up argument for pull up resistor (False = pull down)
    - pause() must be imported from signal()
    - Can get state of button with .is_pressed
    - Seeing a lot of bounce with switch
    - We chose pin 2, which is I2C, so it has 1.8k pullup instead of 50k, so we were hitting noise margin -> bad signals
    - Using pins 17 and 18 fixed this
    - For the joystick, we first connected 5V (in series with a 330 ohm resistor), GND, and Vx. Then, we used a multimeter to confirm that Vx ranged from 0V to 4.8V
    - To scale down to the 3.3V GPIO input range, we used a voltage divider with a 330 and 470 ohm resistor. This stepped us to 0V to 2.8V, well within the 3.3V range, but also above the HIGH input cutoff of 2.0V
    - We used the same button code for the joystick, so that an upwards flick registered as an input

3. Combine all 3 sample scripts and circuit and display the state of all 3 components at the same time
    - We put all three circuits back onto the breadboard
    - It was difficult to plug the joystick directly into the breadboard, so we used the male/female wires to connect them instead
    - Using two event triggers for the joystick/button plus one state variable with the switch worked perfectly in GPIOZero
4. Program the 5 "modes"
    - We decided to use the switch to control between "display mode" and "menu select mode"
    - In menu select mode, the joystick flicks could move the user between 4 different print options, "Fizz", "Buzz", "FizzBuzz" and "Lightyear"
    - In display mode, the button would print the string corresponding to the selected mode
    - If the button was pressed in selection mode or the joystick in display mode, a warning would display
    - Our only issue was passing the state of the program into the event handlers. Base datatypes like integers were unable to be read inside of the function handlers, since they were not within scope
    - To fix, this, we converted the state into an instance of a custom class, and then passed the global state into the handler using the `partial` util from `functools`
        - I.e. `on_button_press = partial(button_press_handler, state)` gives a function call to `button_press_handler` requiring 1 less argument than normal, since the first is filled in to be `state`
    - We also briefly short circuited because two of our wires inadvertently touched (ground and 5V) when we were plugging in 5V. We recommend that people plug these in on opposite ends of the breadboard, not next to each other in the same row, in order to avoid this
    - Lasly, we were experiencing some bouncy input, particularly for our button. Setting the `bounce_time` parameter in the constructor fixed this
    - **Mode clarification**
        - Mode 1: Menu select - button press prints warning
        - Mode 2: Display (fizz) - button press prints fizz
        - Mode 3: Display (buzz) - button press prints buzz
        - Mode 4: Display (fizzbuzz) - button press prints fizzbuzz
        - Mode 5: Display (lightyear) - button press prints lightyear
