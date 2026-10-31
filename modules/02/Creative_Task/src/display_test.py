import pygame
from esp32_serial import Controller

PAC_LEFT, PAC_RIGHT, PAC_UP, PAC_DOWN = 0, 1, 2, 3

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
print("video driver:", pygame.display.get_driver())   # useful for debugging
clock = pygame.time.Clock()
running = True

pacman_ctl = Controller()
pacman_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # 1. Handle window events (required, and gives you a way to quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Read hardware input and update
    pacman_ctl.update()
    if pacman_ctl.is_pressed(PAC_LEFT):
        pacman_pos.x -= 2
    if pacman_ctl.is_pressed(PAC_RIGHT):
        pacman_pos.x += 2
    if pacman_ctl.is_pressed(PAC_UP):
        pacman_pos.y -= 2
    if pacman_ctl.is_pressed(PAC_DOWN):
        pacman_pos.y += 2

    # 3. Draw
    screen.fill("black")
    pygame.draw.circle(screen, "yellow", pacman_pos, 20)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()



