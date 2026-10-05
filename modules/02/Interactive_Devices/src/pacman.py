import pygame
import serial
import time
from esp32_serial import Controller
from maze_map import map, BLOCK_SIZE, MAP_OFFSET_X, MAP_OFFSET_Y

PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN = 0, 1, 2, 3
GHOST_LEFT, GHOST_RIGHT, GHOST_UP, GHOST_DOWN = 4, 5, 6, 7 
PAC_BUTTON, GHOST_BUTTON = 8, 9
SWITCH = 10


# Unit size of wall


# Initialize game
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Scren dimensions are 1280x720
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
running = True

# Speed variables and constants
SLOW_DOWN = .5
DEFAULT_SPEED = 4
speed_scalar_P = 1
speed_scalar_G = 1

# Power-ups variables and constants
POWER_COOLDOWN = 5
POWER_ACTIVE = 3
active_P = False
active_G = False


# Keeps track of times when players used their power ups (start ready to use)
last_power_P = time.monotonic() - (POWER_ACTIVE + POWER_COOLDOWN)
last_power_G = time.monotonic() - (POWER_ACTIVE + POWER_COOLDOWN)


# Initialize hardware input controller
inputs = Controller()

# Wall hitboxes, built once from the map
walls = [pygame.Rect(MAP_OFFSET_X + j*BLOCK_SIZE, MAP_OFFSET_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
         for i, row in enumerate(map) for j, v in enumerate(row) if v == 1]
MAP_W = len(map[0]) * BLOCK_SIZE
MAP_H = len(map) * BLOCK_SIZE

# Player hitboxes (drawn as circles of radius 15)
PLAYER_RADIUS = 15
pacman = pygame.Rect(0, 0, 2*PLAYER_RADIUS, 2*PLAYER_RADIUS)
ghost = pygame.Rect(0, 0, 2*PLAYER_RADIUS, 2*PLAYER_RADIUS)
pacman.center = (MAP_OFFSET_X + 16*BLOCK_SIZE + BLOCK_SIZE//2, MAP_OFFSET_Y + 8*BLOCK_SIZE + BLOCK_SIZE//2)
ghost.center = (MAP_OFFSET_X + 15*BLOCK_SIZE + BLOCK_SIZE//2, MAP_OFFSET_Y + 9*BLOCK_SIZE + BLOCK_SIZE//2)


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


while running:
    inputs.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Power up for pacman (slows down Ghost)
    if inputs.is_pressed(PAC_BUTTON) and (time.monotonic() - (last_power_P + POWER_ACTIVE) > POWER_COOLDOWN):
        active_P = True
        speed_scalar_G = SLOW_DOWN
        last_power_P = time.monotonic()

    if active_P and (time.monotonic() - last_power_P > POWER_ACTIVE):
        active_P = False
        speed_scalar_G = 1

    # Power up for Ghost (slows down Pacman)
    if inputs.is_pressed(GHOST_BUTTON) and (time.monotonic() - (last_power_G + POWER_ACTIVE) > POWER_COOLDOWN):
        active_G = True
        speed_scalar_P = SLOW_DOWN
        last_power_G = time.monotonic()

    if active_G and (time.monotonic() - last_power_G > POWER_ACTIVE):
        active_G = False
        speed_scalar_P = 1


    # Move players, blocked by walls
    move(pacman, *joystick_delta(PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN, speed_scalar_P), walls)
    move(ghost, *joystick_delta(GHOST_LEFT, GHOST_RIGHT, GHOST_UP, GHOST_DOWN, speed_scalar_G), walls)

    # Draw players and map
    screen.fill("black")
    for wall in walls:
        pygame.draw.rect(screen, "white", wall)

    pygame.draw.circle(screen, "yellow", pacman.center, PLAYER_RADIUS) # Pacman
    pygame.draw.circle(screen, "red", ghost.center, PLAYER_RADIUS) # Ghost


    pygame.display.flip()

    clock.tick(60)


