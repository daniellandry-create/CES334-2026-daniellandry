import pygame
import serial
import time
from esp32_serial import Controller

PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN = 1, 2, 3, 4
GHOST_LEFT, GHOST_RIGHT, GHOST_UP, GHOST_DOWN = 5, 6, 7, 8 
PAC_BUTTON, GHOST_BUTTON = 9, 10
SWITCH = 11

pygame.init()
pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

test = Controller()

while running:
    test.update()
    print(test.is_pressed(PAC_LEFT))
    print(test.is_pressed(PAC_RIGHT))
    print(test.is_pressed(PAC_BUTTON))
    time.sleep(1)


