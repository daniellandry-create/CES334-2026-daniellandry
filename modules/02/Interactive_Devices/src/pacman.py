import pygame
import random
import serial
import time
from esp32_serial import Controller
from maze_map import map, BLOCK_SIZE, MAP_OFFSET_X, MAP_OFFSET_Y

PLAYER1_LEFT, PLAYER1_RIGHT, PLAYER1_UP, PLAYER1_DOWN = 0, 1, 2, 3
PLAYER2_LEFT, PLAYER2_RIGHT, PLAYER2_UP, PLAYER2_DOWN = 4, 5, 6, 7 
PLAYER1_BUTTON, PLAYER2_BUTTON = 8, 9

# Each player's inputs as on-screen (left, right, up, down, button).
# Player 1 sits at the bottom of the screen, player 2 at the top facing them,
# so player 2's joystick is reversed: their left is the screen's right, their up is the screen's down.
PLAYER1_CONTROLS = (PLAYER1_LEFT, PLAYER1_RIGHT, PLAYER1_UP, PLAYER1_DOWN, PLAYER1_BUTTON)
PLAYER2_CONTROLS = (PLAYER2_RIGHT, PLAYER2_LEFT, PLAYER2_DOWN, PLAYER2_UP, PLAYER2_BUTTON)
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

# Round variables and constants
NUM_ROUNDS = 6      # Players swap characters every round, so each plays each 3 times
SUDDEN_DEATH_ROUND = NUM_ROUNDS + 1  # Only played if the score is tied after NUM_ROUNDS
ROUND_WINS_NEEDED = 4  # First player to this many round wins takes the game immediately
ROUND_TIME = 90     # Pacman must collect DOTS_TO_WIN dots before this many seconds run out
INTRO_TIME = 2      # Seconds to show "Round N" before players can move

# Dot variables and constants
DOTS_TO_WIN = 5
DOT_MOVE_TIME = 10  # Dot jumps to a new spot if not collected within this many seconds
DOT_RADIUS = 8


# Initialize hardware input controller
inputs = Controller()

# Wall hitboxes, built once from the map
walls = [pygame.Rect(MAP_OFFSET_X + j*BLOCK_SIZE, MAP_OFFSET_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
         for i, row in enumerate(map) for j, v in enumerate(row) if v == 1]
MAP_W = len(map[0]) * BLOCK_SIZE
MAP_H = len(map) * BLOCK_SIZE

# Open tiles where a dot can spawn (skips the border so dots never sit in the wrap-around tunnels)
open_tiles = [(i, j) for i, row in enumerate(map) for j, v in enumerate(row)
              if v == 0 and 0 < i < len(map) - 1 and 0 < j < len(row) - 1]

# Players are drawn as circles with a square hitbox
PLAYER_RADIUS = 15


def tile_center(row, col):
    return (MAP_OFFSET_X + col*BLOCK_SIZE + BLOCK_SIZE//2, MAP_OFFSET_Y + row*BLOCK_SIZE + BLOCK_SIZE//2)


def move(rect, dx, dy, walls, wrap=True):
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

    # Screen edges act as walls when wrapping is disabled
    if not wrap:
        rect.clamp_ip(pygame.Rect(MAP_OFFSET_X, MAP_OFFSET_Y, MAP_W, MAP_H))
        return

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


def power_on(inputs):
    # Switch simulates the power button. Flip the 'not' if your switch is wired the other way.
    return not inputs.is_pressed(SWITCH)


def press_any_button(inputs):
    return inputs.just_pressed(PLAYER1_BUTTON) or inputs.just_pressed(PLAYER2_BUTTON)


def draw_for_both(screen, font, color, dy, text_p1, text_p2=None, bg=None):
    # Player 1 (bottom) reads text_p1 dy pixels below the center line.
    # Player 2 (top) reads text_p2 rotated 180 degrees, dy pixels above the center line.
    if text_p2 is None:
        text_p2 = text_p1
    cx, cy = screen.get_width() // 2, screen.get_height() // 2
    surf_p1 = font.render(text_p1, True, color, bg)
    surf_p2 = pygame.transform.rotate(font.render(text_p2, True, color, bg), 180)
    screen.blit(surf_p1, surf_p1.get_rect(center=(cx, cy + dy)))
    screen.blit(surf_p2, surf_p2.get_rect(center=(cx, cy - dy)))


class MainMenu(Scene):
    def __init__(self):
        self.title_font = pygame.font.Font(None, 120)
        self.prompt_font = pygame.font.Font(None, 48)

    def update(self, inputs):
        if press_any_button(inputs):
            return Gameplay(1, [0, 0])
        return self

    def draw(self, screen):
        screen.fill("black")
        draw_for_both(screen, self.title_font, "yellow", 70, "PAC-MAN")
        draw_for_both(screen, self.prompt_font, "white", 160, "Press any button to start")


class Gameplay(Scene):
    def __init__(self, round_num, scores):
        self.round_num = round_num
        self.scores = scores  # [player 1 score, player 2 score]
        # Sudden death: no catching, no timer, first player to DOTS_TO_WIN dots wins
        self.sudden_death = round_num == SUDDEN_DEATH_ROUND

        # Odd rounds: player 1 is Pacman. Even rounds: player 2 is Pacman.
        if round_num % 2 == 1:
            self.pac_player, self.ghost_player = 0, 1
        else:
            self.pac_player, self.ghost_player = 1, 0
        controls = (PLAYER1_CONTROLS, PLAYER2_CONTROLS)
        self.pac_controls = controls[self.pac_player]
        self.ghost_controls = controls[self.ghost_player]

        self.round_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 40)
        self.hud_font = pygame.font.Font(None, 32)

        # Player hitboxes
        self.pacman = pygame.Rect(0, 0, 2*PLAYER_RADIUS, 2*PLAYER_RADIUS)
        self.ghost = pygame.Rect(0, 0, 2*PLAYER_RADIUS, 2*PLAYER_RADIUS)
        self.pacman.center = tile_center(16, 1)  # Bottom-left corner
        self.ghost.center = tile_center(1, 30)   # Top-right corner

        # Speed and power-up state
        self.speed_scalar_G = 1
        self.active_P = False
        self.active_G = False

        # Keeps track of times when players used their power ups (start ready to use)
        self.last_power_P = time.monotonic() - (POWER_ACTIVE + POWER_COOLDOWN)
        self.last_power_G = time.monotonic() - (POWER_ACTIVE + POWER_COOLDOWN)

        # Round clock starts after the intro
        self.start_time = time.monotonic() + INTRO_TIME

        # Dot Pacman is hunting for (ghost hunts it too in sudden death)
        self.dots = [0, 0]  # Dots collected by [player 1, player 2]
        self.dot = pygame.Rect(0, 0, 2*DOT_RADIUS, 2*DOT_RADIUS)
        self.spawn_dot(self.start_time)

    def spawn_dot(self, now):
        # Center of a random open tile, so the dot never touches a wall. Not on top of a player or its old spot.
        old_center = self.dot.center
        while True:
            self.dot.center = tile_center(*random.choice(open_tiles))
            if self.dot.collidelist([self.pacman, self.ghost]) == -1 and self.dot.center != old_center:
                break
        self.dot_time = now

    def end_round(self, winner):
        scores = self.scores.copy()
        scores[winner] += 1
        return RoundOver(self.round_num, scores, winner)

    def update(self, inputs):
        now = time.monotonic()

        # Freeze players while the round intro is showing
        if now < self.start_time:
            return self

        # Power up for pacman (slows down Ghost)
        if inputs.just_pressed(self.pac_controls[4]) and (now - (self.last_power_P + POWER_ACTIVE) > POWER_COOLDOWN):
            self.active_P = True
            self.speed_scalar_G = SLOW_DOWN
            self.last_power_P = now

        if self.active_P and (now - self.last_power_P > POWER_ACTIVE):
            self.active_P = False
            self.speed_scalar_G = 1

        # Power up for Ghost (Pacman can't wrap around the map edges)
        if inputs.just_pressed(self.ghost_controls[4]) and (now - (self.last_power_G + POWER_ACTIVE) > POWER_COOLDOWN):
            self.active_G = True
            self.last_power_G = now

        if self.active_G and (now - self.last_power_G > POWER_ACTIVE):
            self.active_G = False

        # Move players, blocked by walls
        move(self.pacman, *joystick_delta(*self.pac_controls[:4], 1), walls, wrap=not self.active_G)
        move(self.ghost, *joystick_delta(*self.ghost_controls[:4], self.speed_scalar_G), walls)

        if self.sudden_death:
            # Both players race for the dot; they pass through each other
            for player, rect in ((self.pac_player, self.pacman), (self.ghost_player, self.ghost)):
                if rect.colliderect(self.dot):
                    self.dots[player] += 1
                    if self.dots[player] >= DOTS_TO_WIN:
                        return self.end_round(player)
                    self.spawn_dot(now)
                    break
        else:
            # Ghost caught Pacman: ghost's player wins the round
            if self.pacman.colliderect(self.ghost):
                return self.end_round(self.ghost_player)

            # Pacman collected a dot: count it and move the dot
            if self.pacman.colliderect(self.dot):
                self.dots[self.pac_player] += 1
                if self.dots[self.pac_player] >= DOTS_TO_WIN:
                    return self.end_round(self.pac_player)
                self.spawn_dot(now)

        # Dot moves on its own if it hasn't been collected in time
        if now - self.dot_time >= DOT_MOVE_TIME:
            self.spawn_dot(now)

        # Timer ran out: ghost's player wins the round (no timer in sudden death)
        if not self.sudden_death and now - self.start_time >= ROUND_TIME:
            return self.end_round(self.ghost_player)
        return self

    def draw(self, screen):
        screen.fill("black")
        for wall in walls:
            pygame.draw.rect(screen, "white", wall)

        pygame.draw.circle(screen, "blue", self.dot.center, DOT_RADIUS) # Dot
        pygame.draw.circle(screen, "yellow", self.pacman.center, PLAYER_RADIUS) # Pacman
        pygame.draw.circle(screen, "red", self.ghost.center, PLAYER_RADIUS) # Ghost

        # Each line is drawn twice: upright for player 1 (bottom), upside down for player 2 (top)
        now = time.monotonic()
        if now < self.start_time:
            # Intro covers the middle of the map, so give the text a black background
            if self.sudden_death:
                draw_for_both(screen, self.round_font, "cyan", 45, "Sudden Death!", bg="black")
                draw_for_both(screen, self.small_font, "yellow", 100, f"First to {DOTS_TO_WIN} dots wins", bg="black")
            else:
                roles = ["You are the Ghost", "You are the Ghost"]
                roles[self.pac_player] = "You are Pac-Man"
                draw_for_both(screen, self.round_font, "cyan", 45, f"Round {self.round_num} of {NUM_ROUNDS}", bg="black")
                draw_for_both(screen, self.small_font, "yellow", 100, *roles, bg="black")
        elif self.sudden_death:
            # HUD sits in the open middle rows of the maze
            p1, p2 = self.dots
            draw_for_both(screen, self.hud_font, "cyan", 20,
                          f"You: {p1}/{DOTS_TO_WIN}    Rival: {p2}/{DOTS_TO_WIN}",
                          f"You: {p2}/{DOTS_TO_WIN}    Rival: {p1}/{DOTS_TO_WIN}")
        else:
            time_left = max(0, int(ROUND_TIME - (now - self.start_time) + 0.999))  # Round up so 0:00 shows at the end
            minutes, seconds = divmod(time_left, 60)
            draw_for_both(screen, self.hud_font, "cyan", 20, f"{minutes}:{seconds:02d}    Dots: {self.dots[self.pac_player]}/{DOTS_TO_WIN}")


class RoundOver(Scene):
    def __init__(self, round_num, scores, round_winner):
        self.round_num = round_num
        self.scores = scores
        self.round_winner = round_winner  # 0 = player 1, 1 = player 2
        self.big_font = pygame.font.Font(None, 80)
        self.small_font = pygame.font.Font(None, 48)
        self.prompt_font = pygame.font.Font(None, 36)

        # Game ends as soon as someone reaches ROUND_WINS_NEEDED.
        # A 3-3 tie after the last regular round goes to sudden death, whose winner reaches 4.
        self.game_over = max(scores) >= ROUND_WINS_NEEDED

    def update(self, inputs):
        if press_any_button(inputs):
            if self.game_over:
                return MainMenu()
            return Gameplay(self.round_num + 1, self.scores)
        return self

    def draw(self, screen):
        screen.fill("black")
        p1, p2 = self.scores
        # Headline from each player's point of view: [player 1's text, player 2's text]
        if self.game_over:
            headline = ["You lose", "You lose"]
            headline[self.round_winner] = "You win!"
            prompt = "Press any button to return to the menu"
        elif self.round_num == NUM_ROUNDS:
            headline = ["It's a tie!", "It's a tie!"]
            prompt = "Press any button for sudden death"
        else:
            headline = [f"You lost round {self.round_num}"] * 2
            headline[self.round_winner] = f"You won round {self.round_num}!"
            prompt = "Press any button for the next round"
        draw_for_both(screen, self.big_font, "cyan", 60, *headline)
        draw_for_both(screen, self.small_font, "yellow", 135, f"You: {p1}    Opponent: {p2}", f"You: {p2}    Opponent: {p1}")
        draw_for_both(screen, self.prompt_font, "white", 200, prompt)


scene = MainMenu()

while running:
    inputs.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Switch off: black screen, game frozen. Switching back on restarts like a real power cycle.
    if not power_on(inputs):
        screen.fill("black")
        scene = None
    else:
        if scene is None:
            scene = MainMenu()
        scene = scene.update(inputs)
        scene.draw(screen)

    pygame.display.flip()

    clock.tick(60)
