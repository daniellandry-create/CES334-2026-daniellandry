import pygame
import serial
import time
from esp32_serial import Controller
from maze_map import map, BLOCK_SIZE, MAP_OFFSET_X, MAP_OFFSET_Y

PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN = 0, 1, 2, 3
GHOST_LEFT, GHOST_RIGHT, GHOST_UP, GHOST_DOWN = 4, 5, 6, 7 
PAC_BUTTON, GHOST_BUTTON = 8, 9
SWITCH = 10


# Initialize game
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Scren dimensions are 1280x720
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
running = True

# Speed variables and constants
SLOW_DOWN = .5
DEFAULT_SPEED = 4

# Power-ups variables and constants
POWER_COOLDOWN = 5
POWER_ACTIVE = 3


# Initialize hardware input controller
inputs = Controller()

# Wall hitboxes, built once from the map
walls = [pygame.Rect(MAP_OFFSET_X + j*BLOCK_SIZE, MAP_OFFSET_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
         for i, row in enumerate(map) for j, v in enumerate(row) if v == 1]
MAP_W = len(map[0]) * BLOCK_SIZE
MAP_H = len(map) * BLOCK_SIZE

# Players are drawn as circles with a square hitbox
PLAYER_RADIUS = 15


def tile_center(row, col):
    return (MAP_OFFSET_X + col*BLOCK_SIZE + BLOCK_SIZE//2, MAP_OFFSET_Y + row*BLOCK_SIZE + BLOCK_SIZE//2)


def move(rect, dx, dy, walls):
    # Move one axis at a time so players slide along walls instead of sticking
    rect.x += dx
    for i in rect.collidelistall(walls):
        if dx > 0:
            rect.right = walls[i].left
        elif dx < 0:
            rect.left = walls[i].right
    rect.y += dy
    for i in rect.collidelistall(walls):
        if dy > 0:
            rect.bottom = walls[i].top
        elif dy < 0:
            rect.top = walls[i].bottom

    # Wrap around through the tunnels on the map edges
    if rect.centerx < MAP_OFFSET_X:
        rect.centerx += MAP_W
    elif rect.centerx >= MAP_OFFSET_X + MAP_W:
        rect.centerx -= MAP_W
    if rect.centery < MAP_OFFSET_Y:
        rect.centery += MAP_H
    elif rect.centery >= MAP_OFFSET_Y + MAP_H:
        rect.centery -= MAP_H


def joystick_delta(left, right, up, down, speed):
    step = int(round(DEFAULT_SPEED * speed))
    dx = (inputs.is_pressed(right) - inputs.is_pressed(left)) * step
    dy = (inputs.is_pressed(down) - inputs.is_pressed(up)) * step
    return dx, dy


class Scene:
    # Base class for a screen. update() returns the scene to show next frame.
    def update(self, inputs):
        return self

    def draw(self, screen):
        pass


class MainMenu(Scene):
    def __init__(self):
        self.title_font = pygame.font.Font(None, 120)
        self.prompt_font = pygame.font.Font(None, 48)

    def update(self, inputs):
        if inputs.just_pressed(PAC_BUTTON) or inputs.just_pressed(GHOST_BUTTON):
            return Gameplay()
        return self

    def draw(self, screen):
        screen.fill("black")
        title = self.title_font.render("PAC-MAN", True, "yellow")
        prompt = self.prompt_font.render("Press any button to start", True, "white")
        cx, cy = screen.get_width() // 2, screen.get_height() // 2
        screen.blit(title, title.get_rect(center=(cx, cy - 60)))
        screen.blit(prompt, prompt.get_rect(center=(cx, cy + 40)))


class Gameplay(Scene):
    def __init__(self):
        # Player hitboxes
        self.pacman = pygame.Rect(0, 0, 2*PLAYER_RADIUS, 2*PLAYER_RADIUS)
        self.ghost = pygame.Rect(0, 0, 2*PLAYER_RADIUS, 2*PLAYER_RADIUS)
        self.pacman.center = tile_center(16, 1)  # Bottom-left corner
        self.ghost.center = tile_center(1, 30)   # Top-right corner

        # Speed and power-up state
        self.speed_scalar_P = 1
        self.speed_scalar_G = 1
        self.active_P = False
        self.active_G = False

        # Keeps track of times when players used their power ups (start ready to use)
        self.last_power_P = time.monotonic() - (POWER_ACTIVE + POWER_COOLDOWN)
        self.last_power_G = time.monotonic() - (POWER_ACTIVE + POWER_COOLDOWN)

    def update(self, inputs):
        now = time.monotonic()

        # Power up for pacman (slows down Ghost)
        if inputs.just_pressed(PAC_BUTTON) and (now - (self.last_power_P + POWER_ACTIVE) > POWER_COOLDOWN):
            self.active_P = True
            self.speed_scalar_G = SLOW_DOWN
            self.last_power_P = now

        if self.active_P and (now - self.last_power_P > POWER_ACTIVE):
            self.active_P = False
            self.speed_scalar_G = 1

        # Power up for Ghost (slows down Pacman)
        if inputs.just_pressed(GHOST_BUTTON) and (now - (self.last_power_G + POWER_ACTIVE) > POWER_COOLDOWN):
            self.active_G = True
            self.speed_scalar_P = SLOW_DOWN
            self.last_power_G = now

        if self.active_G and (now - self.last_power_G > POWER_ACTIVE):
            self.active_G = False
            self.speed_scalar_P = 1

        # Move players, blocked by walls
        move(self.pacman, *joystick_delta(PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN, self.speed_scalar_P), walls)
        move(self.ghost, *joystick_delta(GHOST_LEFT, GHOST_RIGHT, GHOST_UP, GHOST_DOWN, self.speed_scalar_G), walls)

        # Ghost caught Pacman: back to the home screen
        if self.pacman.colliderect(self.ghost):
            return MainMenu()
        return self

    def draw(self, screen):
        screen.fill("black")
        for wall in walls:
            pygame.draw.rect(screen, "white", wall)

        pygame.draw.circle(screen, "yellow", self.pacman.center, PLAYER_RADIUS) # Pacman
        pygame.draw.circle(screen, "red", self.ghost.center, PLAYER_RADIUS) # Ghost


scene = MainMenu()

while running:
    inputs.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scene = scene.update(inputs)
    scene.draw(screen)

    pygame.display.flip()

    clock.tick(60)
