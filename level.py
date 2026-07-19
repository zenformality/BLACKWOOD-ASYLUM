# ══════════════════════════════════════════════════════════════════════════════
#  level.py — Map generation, tile queries, and tile interactions
# ══════════════════════════════════════════════════════════════════════════════

from config import MAP_W, MAP_H, TILE


# ── Tile types (in the 2-D list) ────────────────────────────────────────────
#   0  = floor
#   1  = wall
#  'R','B','G','Y' = locked door (wall until matching key used)
#  'kR','kB','kG','kY' = key pickup
#  'note1'..'note5' = story note
#  'h' = health pickup, 'b' = battery pickup
#  'S' = player start (cleared to floor after reading)
#  'E' = exit tile

# ── Carving helpers ──────────────────────────────────────────────────────────

def _carve_room(m, rx, ry, rw, rh):
    """Turn a rectangle of tiles into floor."""
    for y in range(ry, ry + rh):
        for x in range(rx, rx + rw):
            if 0 <= x < MAP_W and 0 <= y < MAP_H:
                m[y][x] = 0


def _add_corridor(m, x1, y1, x2, y2):
    """Carve an L-shaped corridor between two points."""
    x, y = x1, y1
    while x != x2:
        if 0 <= x < MAP_W and 0 <= y < MAP_H:
            m[y][x] = 0
            if y + 1 < MAP_H:
                m[y + 1][x] = 0
        x += 1 if x2 > x else -1
    while y != y2:
        if 0 <= x < MAP_W and 0 <= y < MAP_H:
            m[y][x] = 0
            if x + 1 < MAP_W:
                m[y][x + 1] = 0
        y += 1 if y2 > y else -1


# ── Map generation ──────────────────────────────────────────────────────────

def create_level():
    """
    Build the asylum map and return (tile_map, enemy_spawn_points).

    The map is a MAP_H x MAP_W list of tiles (ints or short strings).
    spawn_points is a list of (tile_x, tile_y, behaviour_string).
    """
    m = [[1] * MAP_W for _ in range(MAP_H)]

    # ── Rooms ────────────────────────────────────────────────────────────────
    _carve_room(m, 1, 12, 8, 6)        # Entrance Hall (start)
    _carve_room(m, 9, 13, 5, 4)        # Corridor East
    _carve_room(m, 14, 11, 8, 8)       # Main Hall
    _carve_room(m, 15, 3, 6, 8)        # North Wing
    _add_corridor(m, 18, 11, 18, 10)
    _add_corridor(m, 18, 19, 18, 20)   # Connect main hall to south wing through green door
    _carve_room(m, 15, 20, 6, 7)       # South Wing
    _add_corridor(m, 18, 19, 18, 20)
    _carve_room(m, 22, 12, 8, 6)       # East Wing
    _add_corridor(m, 22, 14, 21, 14)
    _carve_room(m, 30, 10, 8, 5)       # Far East Wing
    _add_corridor(m, 30, 12, 29, 12)
    _carve_room(m, 22, 22, 8, 6)       # Basement
    _add_corridor(m, 25, 19, 25, 21)
    _carve_room(m, 3, 5, 6, 6)         # Secret Room
    _add_corridor(m, 5, 11, 5, 12)     # Connect secret room to entrance hall
    _add_corridor(m, 5, 10, 5, 11)     # Connect secret room downwards
    _carve_room(m, 30, 20, 8, 7)       # Exit Room
    _add_corridor(m, 30, 22, 29, 22)

    # ── Locked doors ─────────────────────────────────────────────────────────
    m[10][17] = 'R';  m[10][18] = 'R'   # Red door → North Wing
    m[9][17] = 1; m[9][18] = 1          # Wall above red door
    m[11][17] = 1; m[11][18] = 1        # Wall below red door
    m[19][17] = 'G';  m[19][18] = 'G'   # Green door → South Wing
    m[18][17] = 1; m[18][18] = 1        # Wall above green door
    m[20][17] = 1; m[20][18] = 1        # Wall below green door
    m[12][29] = 'B'                       # Blue door → Far East
    m[12][28] = 1; m[12][30] = 1        # Walls left/right of blue door
    m[21][25] = 'Y'                       # Yellow door → Basement
    m[21][24] = 1; m[21][26] = 1        # Walls left/right of yellow door
    m[22][29] = 'B'                       # Blue door → Exit Room
    m[22][28] = 1; m[22][30] = 1        # Walls left/right of exit blue door

    # ── Keys ─────────────────────────────────────────────────────────────────
    m[6][17]  = 'kR'   # Red key  → North Wing
    m[24][26] = 'kY'   # Yellow key → Basement
    m[7][5]   = 'kG'   # Green key → Secret Room
    m[23][17] = 'kB'   # Blue key → South Wing

    # ── Notes ────────────────────────────────────────────────────────────────
    m[14][4]  = 'note1'   # Entrance
    m[14][16] = 'note2'   # Main Hall
    m[17][5]  = 'note3'   # North Wing
    m[15][36] = 'note4'   # Far East
    m[24][24] = 'note5'   # Basement

    # ── Pickups ──────────────────────────────────────────────────────────────
    m[15][5]  = 'h'    # Health  – Entrance
    m[23][26] = 'h'    # Health  – Basement
    m[12][33] = 'h'    # Health  – Far East
    m[6][20]  = 'b'    # Battery – North Wing
    m[25][16] = 'b'    # Battery – South Wing
    m[13][25] = 'b'    # Battery – East Wing
    m[13][36] = 'b'    # Battery – Far East

    # ── Player start & exit ──────────────────────────────────────────────────
    m[14][3] = 'S'
    m[23][36] = 'E'

    # ── Enemy spawn points (tile coords, behaviour) ─────────────────────────
    enemy_spawns = [
        (16, 5,  "patrol"),   # North Wing
        (17, 23, "patrol"),   # South Wing
        (34, 12, "patrol"),    # Far East
        (26, 25, "patrol"),   # Basement
    ]

    return m, enemy_spawns


# ── Tile queries ─────────────────────────────────────────────────────────────

def is_wall_at(rect, tile_map):
    """Return True if rect overlaps any wall or locked-door tile."""
    left   = max(0, int(rect.left // TILE))
    right  = min(MAP_W - 1, int(rect.right // TILE))
    top    = max(0, int(rect.top // TILE))
    bottom = min(MAP_H - 1, int(rect.bottom // TILE))

    for ty in range(top, bottom + 1):
        for tx in range(left, right + 1):
            tile = tile_map[ty][tx]
            if tile == 1:
                return True
            if isinstance(tile, str) and tile in ('R', 'B', 'G', 'Y'):
                return True
    return False


# ── Tile interactions (called each frame) ───────────────────────────────────

def check_tile_pickups(player, tile_map):
    """Auto-pickup health / battery when player stands on them."""
    px = int(player.x // TILE)
    py = int(player.y // TILE)

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            tx, ty = px + dx, py + dy
            if not (0 <= tx < MAP_W and 0 <= ty < MAP_H):
                continue
            tile = tile_map[ty][tx]

            if tile == 'h' and player.hp < player.max_hp:
                player.hp = min(player.max_hp, player.hp + 30)
                tile_map[ty][tx] = 0
                return "pickup_hp"

            if tile == 'b' and player.battery < 100:
                player.battery = min(100, player.battery + 40)
                tile_map[ty][tx] = 0
                return "pickup_bat"

    return None


def try_interact(player, tile_map, story_notes):
    """
    Attempt to interact with a nearby tile (E / Space).
    Returns (event_string, data) or (None, None).

    Events:
      "key"          — picked up a key, data = colour letter
      "note"         — opened a note, data = note dict
      "door_open"    — unlocked a door
      "door_locked"  — door is locked, data = colour letter
      "exit"         — reached the exit
    """
    px = int(player.x // TILE)
    py = int(player.y // TILE)

    for dy in range(-2, 3):
        for dx in range(-2, 3):
            tx, ty = px + dx, py + dy
            if not (0 <= tx < MAP_W and 0 <= ty < MAP_H):
                continue
            tile = tile_map[ty][tx]

            # Keys
            if isinstance(tile, str) and tile.startswith('k'):
                colour = tile[1]
                player.keys.add(colour)
                tile_map[ty][tx] = 0
                return "key", colour

            # Notes
            if isinstance(tile, str) and tile.startswith('note'):
                note_id = tile[4:]  # note1 -> 1, etc.
                full_id = 'note' + note_id
                if full_id in story_notes:
                    player.notes.add(full_id)
                    return "note", story_notes[full_id]

            # Locked doors
            if isinstance(tile, str) and tile in ('R', 'B', 'G', 'Y'):
                if tile in player.keys:
                    tile_map[ty][tx] = 0
                    return "door_open", tile
                else:
                    return "door_locked", tile

            # Exit
            if tile == 'E':
                return "exit", None

    return None, None