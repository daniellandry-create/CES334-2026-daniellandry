# Module 01 - Generative Art
### Daniel Landry

## Summary

For my generative art project, I have put on display a simulation of "Braitenberg's vehicles," which are simple machines that move differently in the face of a light source. Through a surprisingly small number of parameters, complex behavior emerges, and things get really interesting when the complex behaviors of different "vehicles" become dependent on each other, as was achieved in the simulation by making each vehicle a light source itself.

Each vehicle is wired with one of four behaviors, which controls how it turns and how its speed changes relative to the other vehicles on screen:

| Wiring ("personality") | Turns toward light? | Speeds up near light? |
| --- | --- | --- |
| `aggression` | yes | yes |
| `love` | yes | no (slows down) |
| `fear` | no (turns away) | yes |
| `explorer` | no (turns away) | no (slows down) |

## Link to Video:
https://youtu.be/YPwGLgxHahY

## Technical Overview

The sketch is written in JavaScript with p5.js. `setup()` in `sketch.js` creates the canvas and the vehicles, and `draw()` runs every frame, drawing each vehicle as a circle and then calling its `update()` method from `src/vehicle.js`. The background is redrawn each frame with a low alpha value instead of solid black, which is what leaves the fading trails behind the vehicles.

### Screen size, number of vehicles, and vehicle size

Since this was meant to run on whatever display the Pi happens to be plugged into, I didn't want to hard-code how many vehicles there are or how big they are. Both are based on the pixel width of the window when the sketch starts. The number of vehicles is one for every 100 pixels of width, plus 4 so that even a small window has enough going on. The diameter of each vehicle is one pixel for every 50 pixels of width, plus 10 so they never get too small to see. On a 1920 pixel wide monitor, for example, that works out to 23 vehicles that are each 48 pixels across. A bigger screen gets more vehicles instead of just stretching the same few out over more space, so the density looks about the same no matter where it's running.

### Direction

Every vehicle treats every other vehicle as a light source. In `update()`, the vehicle loops through the others and, for each one, takes the vector pointing from itself to that vehicle and divides it by the distance squared. That leaves a vector that points toward the other vehicle with a strength of 1/distance, so nearby vehicles pull a lot harder than far away ones. Adding all of these together gives one combined "light direction" that the vehicle would ideally be facing.

The vehicle doesn't snap to that direction, though. `theta_diff()` uses the dot product to find the angle between where the vehicle is currently heading and the light direction, and the vehicle only turns by a small fraction of that angle each frame (`dir_scalar`, which is 1/75). This is what gives the movement its smooth, curving paths. To know which way to turn, `turn_dir()` looks at the sign of the 2D cross product between the heading and the light direction, which says whether the light is to the left or to the right. The first number in the vehicle's wiring then either keeps that turn (turn toward the light) or flips it (turn away).

### Speed

Speed is based on how close the nearest other vehicle is, since that is the "brightest" light a vehicle can see. That distance is turned into a closeness value between 0 and 1. A vehicle can only "see" a quarter of the screen width (`view_dist` in `update()`), so anything farther than that counts as a closeness of 0, and a vehicle sitting right on top of another has a closeness of 1. The second number in the wiring decides what to do with that value. Aggression and fear multiply `speed_scalar` by the closeness, so they speed up as they get close to something, and love and explorer multiply it by one minus the closeness, so they slow down instead. There is also a small `min_speed` so that nothing ever comes to a complete stop.

I originally measured closeness against half of the screen diagonal. Once there were a lot of vehicles on screen, though, the nearest one was always pretty close compared to that, so the love vehicles were slow the entire time and you couldn't actually see them slowing down near others. Limiting how far they can see fixed that.

### Wrapping around the edges

When a vehicle drives off one side of the screen it comes back on the opposite side. To make this feel continuous, vehicles can also "see" across the edges. `wrapped_offset()` finds the offset from one vehicle to another, and if that gap is more than half the screen width (or height), it means the other vehicle is actually closer by going through the edge, so the width (or height) is added or subtracted to get the shorter path. Both the direction and speed calculations use this offset, so a vehicle near the right edge will react to one near the left edge as if they were right next to each other.

This project was developed and run on a Raspberry Pi.

## Requirements

- A Raspberry Pi running Raspberry Pi OS with the desktop (Wayland), connected to a display.
- Chromium, which comes installed on Raspberry Pi OS.
- No internet connection or build tools are needed, since p5.js is included locally in `p5/`.

## Installation

Clone the repo onto the Pi:

```sh
git clone https://github.com/daniellandry-create/CES334-2026-daniellandry.git
cd CES334-2026-daniellandry/modules/01/generativeArt
```

## Usage

I display the project on the Pi in three parts:

1. **`index.html`** is the page itself. It loads p5.js, `sketch.js`, and `src/vehicle.js`, and the sketch fills the whole window as soon as it opens.
2. **`kiosk.sh`** opens `index.html` in Chromium in kiosk mode, which is full screen with no address bar, tabs, or popups. It also sets the Wayland environment variables Chromium needs so that it can find the display when started from a service instead of a terminal.
3. **`kiosk.service`** is a systemd service that runs `kiosk.sh` once the desktop has loaded, so the art starts on its own every time the Pi boots.

Both `kiosk.sh` and `kiosk.service` have full paths to where the repo lives on my Pi (under the `stu3340` user). If the repo is cloned somewhere else, the `PAGE` path in `kiosk.sh`, and the `User` and `ExecStart` lines in `kiosk.service`, need to be changed to match.

To set it up, copy the service into systemd and enable it:

```sh
sudo cp kiosk.service /lib/systemd/system/
sudo systemctl enable kiosk.service
sudo systemctl start kiosk.service
```

After this, the sketch comes up full screen automatically on every boot. It can be stopped with `sudo systemctl stop kiosk.service`, or turned off at boot with `sudo systemctl disable kiosk.service`.

## Reproducing / Customizing the Design

The main parameters are at the top of `sketch.js` and `src/vehicle.js`:

- `sketch.js`
  - `num_vehicles`: how many vehicles are simulated (based on window width, see above).
  - `vehicle_size`: the diameter, in pixels, each vehicle is drawn at (also based on window width).
  - `options`: the wirings (`aggression`, `love`, `fear`, `explorer`) each vehicle is randomly assigned from.
  - `colors`: the fill color paired with each entry in `options`, by index.
- `src/vehicle.js`
  - `wirings`: defines each behavior as a `[turn toward/away from light, speed up/down near light]` pair. New behaviors can be added here.
  - `speed_scalar`: the top movement speed, in pixels per frame.
  - `min_speed`: the slowest a vehicle is allowed to move.
  - `dir_scalar`: how much of the way toward its target heading a vehicle turns each frame.
  - `view_dist` (inside `update()`): how far a vehicle can see when deciding its speed.

Positions, headings, and wirings all come from random numbers, so no two runs look the same. Refreshing the page gives a new arrangement every time.

## Project Structure

```
generativeArt/
├── index.html      # Page shell; loads p5.js, sketch.js, and vehicle.js
├── sketch.js       # p5 setup()/draw(): creates vehicles and draws each frame
├── kiosk.sh        # Launches the page full screen in Chromium on the Pi
├── kiosk.service   # systemd service that runs kiosk.sh at boot
├── src/
│   └── vehicle.js  # vehicle class: steering, speed, and edge wrapping
├── p5/             # Local copy of the p5.js library
└── assets/         # (unused, reserved for future images/audio)
```

## Credits

- [p5.js](https://p5js.org/), licensed under the GNU LGPL v2.1, included in `p5/`.
- Behavior design inspired by Valentino Braitenberg's *Vehicles: Experiments in Synthetic Psychology* (1984).
