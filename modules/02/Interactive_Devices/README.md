# PVP PacMan - Daniel Landry

### Process:
1. simple hardware inputs with esp32 (joystick calibration)
2. communication of those inputs to RPi (baud rate)
3. communicating with display from RPi
4. Game design
5. Enclosure design

### Noteworthy:

    - Needed correct power adapter
    - When running display program via ssh, RPi doesn't know which screen to display to. You must tell the program to use the Pi's desktop session. The Pi uses Wayland
    - Wayland
