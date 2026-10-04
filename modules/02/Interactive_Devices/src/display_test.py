import pygame
import time
import serial
from esp32_serial import Controller

PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN = 0, 1, 2, 3
GHOST_LEFT, GHOST_RIGHT, GHOST_UP, GHOST_DOWN = 4, 5, 6, 7 
PAC_BUTTON, GHOST_BUTTON = 8, 9
SWITCH = 10

# initialize game
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
dt = 0

pacman_ctl = Controller()

pacman_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:

    screen.fill("black")

    pygame.draw.circle(screen, "yellow", pacman_pos, 20)

    # print(f"Pacman-x = {pacman_pos.x}, Pacman-y = {pacman_pos.y}")

    # Read new hardware inputs
    pacman_ctl.update()

    if pacman_ctl.is_pressed(PAC_LEFT):
        pacman_pos.x -= 2
    if pacman_ctl.is_pressed(PAC_RIGHT):
        pacman_pos.x += 2
    if pacman_ctl.is_pressed(PAC_UP):
        pacman_pos.y -= 2
    if pacman_ctl.is_pressed(PAC_DOWN):
        pacman_pos.y += 2
    

    #update screen
    pygame.display.flip()

    pygame.time.Clock().tick(60)




