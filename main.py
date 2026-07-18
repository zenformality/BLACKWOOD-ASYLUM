# ══════════════════════════════════════════════════════════════════════════════
#  BLACKWOOD ASYLUM — Entry Point
#  A Top-Down Horror Survival Game
#
#  Run with:  py main.py
#  Requires:  Python 3.x + pygame
# ══════════════════════════════════════════════════════════════════════════════

import sys
import os

# Make sure the horror/ folder is on the path so our modules import cleanly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame

# ── Initialise pygame display FIRST (fonts need the display) ────────────────
pygame.init()
pygame.mixer.init()

from config import W, H, init_fonts
init_fonts()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("BLACKWOOD ASYLUM")

from assets import init_sounds, init_images
init_sounds()
init_images()

# ── Go! ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from game import Game
    g = Game(screen)
    g.run()
    sys.exit()
