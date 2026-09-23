# Module 01 - Generative Art
### Daniel Landry

## Summary

For my generative art project, I have put on display a simulation of "Braitenberg's vehicles," which are simple machines that move differently in the face of a light source. Through a surprisingly small number of parameters, complex behavior emerges, and things get really interesting when the complex behaviors of different "vehicles" become dependent on each other, as was achieved in the simulation by making each vehicle a light source itself.

Each vehicle is wired with one of four behaviors, which controls how it turns and accelerates relative to the combined pull of every other vehicle on screen:

| Wiring ("personality") | Turns toward light? | Speeds up near light? |
| `aggression` | yes | yes |
| `love` | yes | no (slows down) |
| `fear` | no (turns away) | yes |
| `explorer` | no (turns away) | no (slows down) |

## Technical Overview

The sketch is built with p5.js and JavaScript. `p5.js`'s `setup()`/`draw()` loop drives the animation:

- `setup()` (in `sketch.js`) creates the canvas and instantiates a fixed number of `vehicle` objects at random positions, headings, and wirings.
- `draw()` (in `sketch.js`) draws every vehicle as a circle, then calls its `update()` method.
- `vehicle.update()` (in `src/vehicle.js`) treats every other vehicle as a light source. For each one, it computes a vector pointing toward it, weighted by the inverse square of the distance, and sums these into a single combined "light direction." It then turns the vehicle toward or away from that direction (depending on wiring), scales speed up or down based on the light's intensity, and wraps the vehicle's coordinates around the edges of the canvas.

This project was developed and run on a Raspberry Pi.

## Requirements

- Any modern desktop browser (Chrome, Firefox, Safari, Edge). No installation, build tools, or internet connection are required — p5.js is vendored locally in `p5/`.
- Optional, for serving the page over HTTP instead of opening the file directly: Python 3 (ships with macOS/Linux) or the [VS Code Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer).

## Installation

```sh
git clone https://github.com/daniellandry-create/CES334-2026-daniellandry.git
cd CES334-2026-daniellandry/modules/01/generativeArt
```

No `npm install` is needed — `p5.min.js` is already included in this directory.

## Usage

This is a static site, so any of the following works:

**Option A — open the file directly**
```sh
open index.html      # macOS
```
or double-click `index.html` in a file browser.

**Option B — serve it locally (recommended if you plan to add assets/images/audio later, since browsers block local file access for those)**
```sh
python3 -m http.server 8000
```
Then visit `http://localhost:8000` in a browser.

**Option C — VS Code Live Server**
Open the folder in VS Code, install the Live Server extension, right-click `index.html`, and choose "Open with Live Server."

The sketch fills the browser window and starts animating immediately — no interaction is required.

## Reproducing / Customizing the Design

All tunable parameters live at the top of `sketch.js` and `src/vehicle.js`:

- `sketch.js`
  - `num_vehicles` — how many vehicles are simulated.
  - `options` — the pool of wirings (`aggression`, `love`, `fear`, `explorer`) each vehicle is randomly assigned from.
  - `colors` — the fill color paired with each entry in `options`, by index.
  - `vehicle_size` — the diameter, in pixels, each vehicle is drawn at.
- `src/vehicle.js`
  - `wirings` — defines each behavior as a `[turn toward/away from light, speed up/down near light]` pair; add new entries here to create new behaviors.
  - `speed_scalar` — base movement speed.
  - `dir_scalar` — how quickly a vehicle turns toward its target heading each frame.

Because the simulation is seeded from `Math.random()`, no two runs look identical; re-running or refreshing the page produces a new arrangement of vehicles every time.

## Project Structure

```
generativeArt/
├── index.html          # Page shell; loads p5.js, vehicle.js, then sketch.js
├── sketch.js            # p5 setup()/draw() — creates vehicles and draws each frame
├── src/
│   └── vehicle.js        # vehicle class: movement, steering, and light-following logic
├── p5/                    # Vendored p5.js library (no external dependency)
└── assets/               # (unused — reserved for any future images/audio)
```

## Credits

- [p5.js](https://p5js.org/) — licensed under the GNU LGPL v2.1, vendored in `p5/`.
- Behavior design inspired by Valentino Braitenberg's *Vehicles: Experiments in Synthetic Psychology* (1984).
