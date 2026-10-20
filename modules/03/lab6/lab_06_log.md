# Creative Embedded Systems Lab 6 Log

Ryan Fernandes and Daniel Landry

## Demo Video:

Watch it on [YouTube here](https://youtu.be/n3K2km8LFvo)!

## Action Plan
1. Research how to communicate data from esp to RPi via wifi
2. Connect esp to wifi
3. Write simple script that sends single message from esp to pi on boot
4. Wire photoresistor
5. Add websockets server to raspberry pi server
6. Connect p5.js visualization


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
10. Connected pi to yale wireless and succesfully tested manually sending data from laptop with the `nc -u` command—very demonstrative!
11. Brainstormed ideas for representing changing light with pi other than terminal output (bees, atoms, seasons)
12. On Sunday, tested ESP32 WiFi connection again, and it was working on yale wireless (seems like time was just needed for MAC address to be registered with Yale IT)
13. Tested single message send to ESP32—worked very well
14. Wired photoresistor with 3.3k-ohm resistor above ADC and photoresistor below
15. Added code to ESP32 script to use analogRead, clamping, and scaling to 0.0-1.0 range
16. Sent values in loop to Raspberry Pi and printed to terminal in Pi server script
17. Set up websockets server in the existing server.py file. Be careful with blocking operations! UDP reception (and possibly sends) are blocking in Python, so need to use asyncio.to_thread()
18. Set up p5.js frontend and websocket connection, had the wrong port at first, so client was not connecting, but it was a simple fix
19. Did a simple proof of concept with events sent as JSON objects from websocket server to client
20. Tests worked, so created scaffolding for the image fade and used AI to add better styling/cover image
21. Tested full system, and we realized that no image showed when the page first loaded -> this was because no event had been trigerred yet
22. Updated sketch.js to send a request message to the websockets server on init, and had websockets server respond by sending a dummy update event for its current state
