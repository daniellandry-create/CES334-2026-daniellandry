# Lab Log - Ryan and Daniel

## Action Plan
1. Review how to connect ESP32 to Arduno IDE
2. Plug and test serial communication with ESP32 
4. Get mac address from ESP32 
5. Write and run programs to test digital and analog input from button, switch, and joystick
6. Setup and test serial communication between ESP32 and raspberrypi 

## Execution
1. ESP32 USB port (not UART) is used when you wnat the ESP to emulate a USB Device (mouse, keyboard, hardrive)
2. Created test_serial.ino program that pints to serial output
3. Connected laptop to ESP via UART
4. Upon running program, recieved fatal error concerning incorrect board selection
    - selected: ESP32 DevModule
    - correct version: ESP32S# DevModule 
5. After changing board selection program ran as intended, printing "Looping..." repeatedly
6. Gibberish appears upon reseting ESP32 because ROM bootloader messages sent to arduino IDE 
are on default, hardcoded 115200 baud rate (as opposed to 9600), fix maybe with delay() at start
7. Note: For arduino programs, directory must have same name as main .ino program
8. Created mac_address directory and program
9. Mac Address (Ryan): 14:C1:9F:38:B3:68
10. Wired up joystick using A3 pin on board. Joystick program reads analog value using analogRead() and prints it to serial output
11. Wired up button and switch with a closed circuit connecting to ground and internal pull-up
12. Ran into errors during testing due to poor connection between ESP32 pins and breadboard
13. Input 5V to joystick and put both x and y-outputs through roughly 3/5 voltage divider
14. Note: Analog inputs are ints, not floats
15. Created lab4_serial.py
16. Used serial.Serial('NAME', 9600)


