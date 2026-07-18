# ══════════════════════════════════════════════════════════════════════════════
#  config.py — All constants, colors, fonts, and paths
# ══════════════════════════════════════════════════════════════════════════════

import os
import pygame

# ── Window ───────────────────────────────────────────────────────────────────
W, H = 1024, 768
FPS = 60

# ── Tile / Map ───────────────────────────────────────────────────────────────
TILE = 48
MAP_W, MAP_H = 40, 30  # tiles

# ── Asset Directory ──────────────────────────────────────────────────────────
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# ── Colors ───────────────────────────────────────────────────────────────────
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
RED         = (200, 30, 30)
DARK_RED    = (120, 10, 10)
BLOOD_RED   = (139, 0, 0)
CRIMSON     = (220, 20, 60)
DARK_GREEN  = (0, 80, 0)
GREEN       = (0, 200, 0)
BLUE        = (30, 80, 180)
YELLOW      = (255, 220, 50)
ORANGE      = (255, 140, 0)
GREY        = (80, 80, 80)
DARK_GREY   = (40, 40, 40)
LIGHT_GREY  = (150, 150, 150)
WALL_COLOR  = (50, 50, 55)
FLOOR_COLOR = (25, 25, 28)
DOOR_COLOR  = (100, 70, 30)
KEY_RED     = (220, 50, 50)
KEY_BLUE    = (50, 100, 220)
KEY_GREEN   = (50, 200, 80)
KEY_YELLOW  = (220, 200, 50)

# ── Fonts ────────────────────────────────────────────────────────────────────
font_huge  = None
font_big   = None
font_mid   = None
font_small = None
font_tiny  = None
font_note  = None
font_note_b = None


def init_fonts():
    global font_huge, font_big, font_mid, font_small, font_tiny, font_note, font_note_b
    font_huge    = pygame.font.SysFont("Georgia", 72, bold=True)
    font_big     = pygame.font.SysFont("Georgia", 48, bold=True)
    font_mid     = pygame.font.SysFont("Georgia", 28, bold=True)
    font_small   = pygame.font.SysFont("Georgia", 20)
    font_tiny    = pygame.font.SysFont("Georgia", 16)
    font_note    = pygame.font.SysFont("Courier New", 18)
    font_note_b  = pygame.font.SysFont("Courier New", 18, bold=True)
