# PVP PacMan - Daniel Landry
### Pacman except it's you versus your friend!

## Project Overview
The project I took on for my Creative Embedded Systems class "Interactive Devices" module assignment was to design and build a portable, person vs. person Pacman game that lets one share the thrill of the classic arcade game with a friend, partner, or family member! The project combines hardware and software to create a box-shaped gaming console with controls on either side, like a simple, specialized version of the consoles we have today such as Xbox and PlayStation. The two players sit across from each other with the screen lying between them, so each person plays from their own side of the board.

Here is the device in action (video link): https://youtu.be/x-odvNzbe3I

## Rules
Before diving into the technical side of the project, a brief summary of the rules might make the technical flow easier to understand.

1. The general setup and concept is similar (but not identical) to the original Pacman: there is one Pacman, one ghost, and a map with walls scattered throughout. A brand new random map is made at the start of every game.
2. Unlike the original, there is only one dot on the map at any given time, and the Pacman must collect it. It moves to a different random position every 10 seconds, or when the Pacman collects it, whichever comes first.
3. Each game is best-of-7 rounds. For the first 6 rounds (or until someone wins 4), the two players alternate between being the ghost and being the Pacman, so each player gets 3 turns as each character. The 7th round (if necessary) is a sudden death round.
4. To win a round, the Pacman must collect 5 dots without being caught by the ghost and before the timer, initially set at 1:30, runs out. The ghost must either catch the Pacman or defend until time expires. In the case of a sudden death round, the first player to 5 dots wins (the ghost can no longer catch the Pacman, and the two characters pass right through each other).
5. Each character has their own power-up, activated by a push-button. The Pacman's power-up slows down the ghost to half speed for three seconds. The ghost's power-up blocks the Pacman from using the wrap-around tunnels for three seconds, so the edges of the screen act like walls. After a power-up is used, it has a five second cooldown before it can be used again. Neither character has a power-up in a sudden death round.
6. Each player always starts in their own corner of the map, no matter which character they are playing that round.

## Technical Overview
Before covering the software, I would like to quickly cover all hardware that was used in this project, since it makes up the inputs and outputs of the programs in the codebase.

### Electronics

| Part | Quantity | Purpose |
| --- | --- | --- |
| Joystick | 2 | Player movement |
| Push-button | 2 | Player power-ups |
| Switch | 1 | On/off switch for the game |
| 7" LCD HDMI display | 1 | Shows the game |
| ESP32-S3-DevKitC-1 | 1 | Reads all of the hardware inputs |
| Raspberry Pi 5 | 1 | Runs the game and sends it to the display over HDMI |

The ESP32 and the Pi are connected by USB, which is how the ESP32 sends the state of the controls to the Pi over serial.

These are the ESP32 pins each input is wired to (set at the top of `src/main.cpp`):

| Input | ESP32 pin(s) |
| --- | --- |
| Player 1 joystick (x, y) | GPIO 4, GPIO 5 |
| Player 2 joystick (x, y) | GPIO 1, GPIO 2 |
| Player 1 button | GPIO 6 |
| Player 2 button | GPIO 7 |
| Switch | GPIO 15 |

The buttons and the switch use the ESP32's internal pull-up resistors, so they read `LOW` when pressed.

### Software
Some of the programs in this codebase run on the ESP32, and some run on the Pi. The ESP32's only job is to read the controls and send them to the Pi. The Pi does everything else.

#### ESP32: `src/main.cpp`
This is built and uploaded with PlatformIO (the settings are in `platformio.ini`). Every 5 milliseconds, the ESP32 reads both joysticks, both buttons, and the switch, and packs all of them into a single 16-bit number, where each bit is one input:

| Bits | Input |
| --- | --- |
| 0-3 | Player 1 left, right, up, down |
| 4-7 | Player 2 left, right, up, down |
| 8 | Player 1 button |
| 9 | Player 2 button |
| 10 | Switch |

The joysticks are analog, but the game only needs to know which directions are being pushed, so `readJoystick()` turns each axis into on/off directions. The middle of the joystick's range reads about 1800, and anything within 1000 of that counts as neutral. Past that, the direction's bit is turned on. Pushing diagonally turns on two bits at once, which is how the characters can move diagonally.

The number is then sent to the Pi as text, one number per line, with `Serial.println()`.

#### Pi: `src/esp32_serial.py`
The `Controller` class reads those lines from the serial port (`/dev/ttyUSB0` at 115200 baud) and keeps track of the latest state. The game calls `update()` once per frame, and then asks `is_pressed(bit)` or `just_pressed(bit)` about any input.

A few details make this reliable:
- The serial data doesn't always arrive in full lines, so any partial line is saved in a buffer until the rest of it shows up on the next frame.
- If several lines arrived since the last frame, only the newest valid one is used, and garbled lines are skipped.
- If no valid line has arrived for 0.2 seconds (for example, if the USB cable comes loose), every input is treated as released, so the characters don't keep running on their own.
- `just_pressed()` compares against the previous frame, so it is only true on the frame a button first goes down. The game uses this for the buttons so that holding a button doesn't keep firing the power-up, and so that the press used to start a round doesn't also trigger a power-up.

#### Pi: `src/pacman.py`
This is the game itself, written with Pygame. It runs at 60 frames per second, and every frame it reads the controller, updates the game, and draws it.

**Screens.** Each screen of the game is its own class: `MainMenu`, `Gameplay` (one round), and `RoundOver` (the screen between rounds, and the final results). Each one has an `update()` method that returns which screen should be shown on the next frame, and a `draw()` method. The main loop just keeps track of the current screen. A new `Gameplay` is created for every round, so things like positions, timers, and power-ups reset on their own, while the score and the map are passed along from round to round.

**Movement and walls.** Both characters are drawn as circles, but they move as square hitboxes (`pygame.Rect`), since Pygame can check rectangles against each other easily. `move()` moves a character left/right first and pushes it back out of any wall it ran into, then does the same for up/down. Handling the two directions separately lets a character slide along a wall instead of getting stuck on it. After that, any character that went off one edge of the screen comes back on the opposite edge, which is how the wrap-around tunnels work.

**Two players on opposite sides.** Since the players sit across from each other, player 2 sees everything upside down. To fix this, player 2's joystick is reversed in `PLAYER2_CONTROLS`, so that pushing left moves their character to their left. All of the text is also drawn twice by `draw_for_both()`: once below the middle of the screen for player 1, and once rotated 180 degrees above the middle for player 2. Some text is different for each player, like "You are Pac-Man" and "You are the Ghost", or "You win!" and "You lose".

**Power-ups.** Power-up state belongs to the player, not the character. Each player's button triggers whatever their character can do that round. Each player has an icon on the border on their side of the screen, which is green when their power-up is ready and red while it's being used or cooling down. In a sudden death round, power-ups are turned off and both icons are gray.

**On/off switch.** When the switch is turned off, the screen goes black and the game stops. Turning it back on restarts at the main menu, like turning a real console off and on.

Most of the numbers that control the game (round time, dots needed to win, power-up length and cooldown, speeds, and more) are constants at the top of the file, so they are easy to tweak.

#### Pi: `src/maze_map.py`
This file builds a new random map for every game. The map is 18 rows by 32 columns of 40 pixel tiles, which exactly fills the 1280 x 720 screen. Each map follows these rules:

- There is a solid border with four wrap-around tunnels: one on the left, right, top, and bottom.
- Walls are only made of straight bars, L-shapes, and small blocks, and no two wall pieces ever touch (not even diagonally). This means walls can never join into U-shapes, so there are no dead ends that a Pacman could get trapped in.
- Every open tile can be reached from every other open tile.
- The map is mirrored left-to-right and top-to-bottom, so neither player's side of the board has an advantage.

To build a map, only the top-left quarter is generated, by trying to place random wall pieces many times and keeping only the ones that don't touch anything. That quarter is then mirrored into the other three. As a final check, `is_valid()` makes sure there are no dead ends and that every tile can be reached, and a new map is made if it fails. The original hand-made map is also still in this file as `MAP_STRINGS`.

#### Other files
- `src/run_pacman.sh` starts the game on the Pi (see Usage below).
- `src/display_test.py` is a small test I used early on to make sure the Pi could read the controller and draw to the display. It moves a single circle around with player 1's joystick.

## Requirements
- An ESP32-S3-DevKitC-1, wired as shown above.
- A computer with PlatformIO (I used the VS Code extension) to upload the ESP32 code.
- A Raspberry Pi running Raspberry Pi OS with the desktop (Wayland), connected to the display.
- Python 3 on the Pi with `pygame` and `pyserial`.

## Installation
Clone the repo:

```sh
git clone https://github.com/daniellandry-create/CES334-2026-daniellandry.git
cd CES334-2026-daniellandry/modules/02/Interactive_Devices
```

Upload the controller code to the ESP32 with PlatformIO, either with the Upload button in VS Code or from the terminal:

```sh
pio run --target upload
```

On the Pi, install the Python libraries:

```sh
pip install pygame pyserial
```

## Usage
Plug the ESP32 into the Pi with USB, then start the game on the Pi:

```sh
./src/run_pacman.sh
```

The game opens full screen on the main menu. Either player can press their button to start.

`run_pacman.sh` sets the `XDG_RUNTIME_DIR` and `WAYLAND_DISPLAY` environment variables before starting the game. Without them, the game can't find the Pi's display when it's started over SSH (see below). If you use a Python virtual environment, change `python3` in the script to your environment's Python.

## Noteworthy
- **Power supply:** the Pi 5 needs the correct power adapter. With the wrong one, it doesn't get enough power to run everything reliably.
- **Running over SSH:** when the game is started over SSH, the Pi doesn't know which screen to display on. The program has to be told to use the Pi's desktop session, which on the Pi uses Wayland. That's what the two environment variables in `run_pacman.sh` do.
- **Serial port name:** the controller code expects the ESP32 at `/dev/ttyUSB0`. If the Pi gives it a different name (for example `/dev/ttyACM0`), change the `port` in `Controller` in `esp32_serial.py`.
- **Switch direction:** depending on how the switch is wired, "on" and "off" might be backwards. If so, remove the `not` in `power_on()` in `pacman.py`.
