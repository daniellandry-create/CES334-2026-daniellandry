import pygame
import serial
import time
from esp32_serial import Controller

PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN = 0, 1, 2, 3
GHOST_LEFT, GHOST_RIGHT, GHOST_UP, GHOST_DOWN = 4, 5, 6, 7 
PAC_BUTTON, GHOST_BUTTON = 8, 9
SWITCH = 10

# Initialize game
pygame.init()
pygame.display.set_mode((1280, 720))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
running = True

# Initialize Pacman player
pacman = Controller()
pacman_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Initialize Ghost layer
ghost = Controller()
ghost_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# For ghost slow-down power
speed_scalar = 1

while running:
    test.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    # Calculate Pacman position
    if pacman_ctl.is_pressed(PAC_LEFT):
        pacman_pos.x -= 2 * speed_scalar
    if pacman_ctl.is_pressed(PAC_RIGHT):
        pacman_pos.x += 2 * speed_scalar
    if pacman_ctl.is_pressed(PAC_UP):
        pacman_pos.y -= 2 * speed_scalar
    if pacman_ctl.is_pressed(PAC_DOWN):
        pacman_pos.y += 2 * speed_scalar

    # Calculate ghost position
    if ghost_ctl.is_pressed(GHOST_LEFT):
        ghost_pos.x -= 2
    if ghost_ctl.is_pressed(GHOST_RIGHT):
        ghost_pos.x += 2
    if ghost_ctl.is_pressed(GHOST_UP):
        ghost_pos.y -= 2
    if ghost_ctl.is_pressed(GHOST_DOWN):
        ghost_pos.y += 2

    # Draw players and map
    screen.fill("black")
    pygame.draw.circle(screen, "yellow", pacman_pos, 10) # Pacman
    pygame.draw.circle(screen, "yellow", ghost_pos, 10) # Ghost


    pygame.display.flip()

    clock.tick(60)


