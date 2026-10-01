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
 

