#18 rows x 32 columns, 40x40 px tiles = exactly 1280 x 720, no offset needed.
# 1 = wall, 0 = open.
# Wrap-around gaps: top/bottom at columns 15-16, left/right at rows 8-9.

import random

BLOCK_SIZE = 40
MAP_OFFSET_X = 0
MAP_OFFSET_Y = 0
ROWS = 18
COLS = 32

# Original hand-made map, kept for reference / testing
MAP_STRINGS = [
    "11111111111111100111111111111111",
    "10000000000000000000000000000001",
    "10111110010011100111001001111101",
    "10000000010000000000001000000001",
    "10111011010000000000001011011101",
    "10100011000111100111100011000101",
    "10100000000010000001000000000101",
    "10001111100000000000000111110001",
    "00000000000000000000000000000000",
    "00000000000000000000000000000000",
    "10001111100000000000000111110001",
    "10100000000010000001000000000101",
    "10100011000111100111100011000101",
    "10111011010000000000001011011101",
    "10000000010000000000001000000001",
    "10111110010011100111001001111101",
    "10000000000000000000000000000001",
    "11111111111111100111111111111111",
]

# Same data structure as before: a list of rows, each a list of ints
map = [[int(ch) for ch in row] for row in MAP_STRINGS]


# ---------------- Random map generation ----------------
# Rules:
#   - Solid border with four wrap-around tunnels (same spots as the map above)
#   - Wall pieces are only bars, L-shapes, and blocks, and never touch each other
#     (not even diagonally) or the border, so they can't merge into U-shapes
#   - That also means no dead ends, and every open tile is reachable
#   - Mirrored left/right and top/bottom so neither player's side has an advantage

QUAD_ROWS = ROWS // 2   # One quarter of the map is generated, then mirrored
QUAD_COLS = COLS // 2
PLACE_ATTEMPTS = 400    # More attempts = denser maze


def random_piece():
    # Returns a list of (row, col) offsets for one wall piece
    kind = random.choice(["hbar", "hbar", "vbar", "L", "L", "block"])
    if kind == "hbar":
        return [(0, c) for c in range(random.randint(1, 5))]
    if kind == "vbar":
        return [(r, 0) for r in range(random.randint(2, 4))]
    if kind == "block":
        h, w = random.choice([(2, 2), (2, 3)])
        return [(r, c) for r in range(h) for c in range(w)]
    # L-shape: horizontal and vertical arm sharing a corner, in any of 4 orientations
    across, down = random.randint(2, 4), random.randint(2, 3)
    sr, sc = random.choice([1, -1]), random.choice([1, -1])
    cells = {(0, sc*c) for c in range(across)} | {(sr*r, 0) for r in range(down)}
    return list(cells)


def mirror(quad):
    # Mirror the top-left quarter into a full map, left/right and top/bottom
    return [[quad[r if r < QUAD_ROWS else ROWS - 1 - r][c if c < QUAD_COLS else COLS - 1 - c]
             for c in range(COLS)] for r in range(ROWS)]


def open_neighbors(grid, r, c):
    # Open tiles next to (r, c), following the wrap-around tunnels
    result = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = (r + dr) % ROWS, (c + dc) % COLS
        if grid[nr][nc] == 0:
            result.append((nr, nc))
    return result


def is_valid(grid):
    open_tiles = [(r, c) for r in range(ROWS) for c in range(COLS) if grid[r][c] == 0]
    # No dead ends: every open tile has at least 2 ways out
    if any(len(open_neighbors(grid, r, c)) < 2 for r, c in open_tiles):
        return False
    # Every open tile reachable from every other
    seen = {open_tiles[0]}
    stack = [open_tiles[0]]
    while stack:
        for n in open_neighbors(grid, *stack.pop()):
            if n not in seen:
                seen.add(n)
                stack.append(n)
    return len(seen) == len(open_tiles)


def random_map():
    while True:
        quad = [[0] * QUAD_COLS for _ in range(QUAD_ROWS)]
        for c in range(QUAD_COLS):
            quad[0][c] = 1                  # Top border
        for r in range(QUAD_ROWS):
            quad[r][0] = 1                  # Left border
        quad[0][QUAD_COLS - 1] = 0          # Top/bottom tunnel (columns 15-16)
        quad[QUAD_ROWS - 1][0] = 0          # Left/right tunnel (rows 8-9)

        # Pieces stay 1 tile from the border and from the mirror lines,
        # so they never touch the border or their own mirrored copy
        for _ in range(PLACE_ATTEMPTS):
            r0, c0 = random.randint(2, QUAD_ROWS - 2), random.randint(2, QUAD_COLS - 2)
            cells = [(r0 + dr, c0 + dc) for dr, dc in random_piece()]
            if not all(2 <= r <= QUAD_ROWS - 2 and 2 <= c <= QUAD_COLS - 2 for r, c in cells):
                continue
            # Every cell and its 8 surrounding tiles must be empty (keeps pieces apart)
            if any(quad[r + dr][c + dc] for r, c in cells for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                continue
            for r, c in cells:
                quad[r][c] = 1

        grid = mirror(quad)
        if is_valid(grid):
            return grid
