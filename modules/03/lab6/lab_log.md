# Creative Embedded Systems Lab 6 Log

## Action Plan
1. Research how to communicate data from esp to RPi via wifi
2. Connect esp to wifi
3. Write simple script that sends single message from esp to pi on upload of program

## Execution
1. Confirmed esp32 in good health
2. Used the following link for researching how to set up wifi connection from esp32: https://www.aranacorp.com/en/udp-communication-between-raspberry-pi-and-esp32/
3. Registered mac address of esp32 on Yale Network Registration Portal: https://reg.its.yale.edu/drp/devices/login
4. Wrote scipt to test esp WiFi connection, but esp32 wouldn't connect (loaded indefinitely)
5. Tested connecting to YaleGuest WiFi instead, and successfully connected
6. Shifting to setting up pi as host by writing script to create socket on pi
7. Pi script uses s.connect("8.8.8.8", 80) to "fake" connect to an arbitrary (but known) remote host through the wifi network to detmine assigned IP.
9. data,addr = sock.recvfrom(bufferSize) - collects data and address message sent to RPi port from esp.
9. sock.sendto("RPI recieved OK", addr) - sends acknowledgment back to client
10. Connected pi to yale wireless and succesfully tested manually sending data from laptop
11. Brainstormed ideas for representing changing light with pi other than terminal output (bees, atoms, seasons)
