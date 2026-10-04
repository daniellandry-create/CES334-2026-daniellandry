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
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Scren dimensions are 1024 X 600
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
running = True


# Initialize hardware input controller
inputs = Controller()

# Initialize player positions
print(screen.get_width())
print(screen.get_height())
pacman_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ghost_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# For ghost slow-down power
speed_scalar = 1

while running:
    inputs.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
     #if inputs.is_pressed(PAC_BUTTON):


    # Calculate Pacman position
    if inputs.is_pressed(PAC_LEFT):
        pacman_pos.x -= 2 * speed_scalar
    if inputs.is_pressed(PAC_RIGHT):
        pacman_pos.x += 2 * speed_scalar
    if inputs.is_pressed(PAC_UP):
        pacman_pos.y -= 2 * speed_scalar
    if inputs.is_pressed(PAC_DOWN):
        pacman_pos.y += 2 * speed_scalar

    # Calculate ghost position
    if inputs.is_pressed(GHOST_LEFT):
        ghost_pos.x -= 2 * speed_scalar
    if inputs.is_pressed(GHOST_RIGHT):
        ghost_pos.x += 2 * speed_scalar
    if inputs.is_pressed(GHOST_UP):
        ghost_pos.y -= 2 * speed_scalar
    if inputs.is_pressed(GHOST_DOWN):
        ghost_pos.y += 2 * speed_scalar

    # Draw players and map
    screen.fill("black")
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 1:
                pygame.draw.rect(screen, "white", (BLOCK_SIZE*j, BLOCK_SIZE*i, BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.circle(screen, "yellow", pacman_pos, 15) # Pacman
    pygame.draw.circle(screen, "red", ghost_pos, 15) # Ghost


    pygame.display.flip()

    clock.tick(60)


