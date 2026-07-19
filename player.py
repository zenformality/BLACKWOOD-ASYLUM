# ══════════════════════════════════════════════════════════════════════════════
#  player.py — Player character class
# ══════════════════════════════════════════════════════════════════════════════

import math
import random
import pygame

from assets import snd_footstep, snd_hurt, snd_sanity_low
from level import is_wall_at


class Player:
    """The detective the player controls."""

    def __init__(self, x, y):
        # Position (pixels, float)
        self.x = float(x)
        self.y = float(y)
        self.speed = 3.0

        # Stats
        self.hp = 100
        self.max_hp = 100
        self.sanity = 100
        self.max_sanity = 100
        self.battery = 100

        # Flashlight
        self.flashlight_on = True
        self.flashlight_radius = 220

        # Inventory
        self.keys = set()    # e.g. {"R", "B"}
        self.notes = set()   # e.g. {"1", "3"}

        # State
        self.facing = 0.0        # radians (toward mouse)
        self.hurt_timer = 0      # flash when hit
        self.invuln_timer = 0    # i-frames
        self.footstep_timer = 0
        self.sanity_timer = 0    # sanity sound cooldown
        self.bob = 0.0           # walk animation offset
        self.alive = True

    # ── Helpers ──────────────────────────────────────────────────────────────

    def get_rect(self):
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20)

    def take_damage(self, amount):
        if self.invuln_timer > 0:
            return
        self.hp -= amount
        self.hurt_timer = 30
        self.invuln_timer = 45
        snd_hurt.play()
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    # ── Update (called every frame) ─────────────────────────────────────────

    def update(self, keys_pressed, tile_map, camera_x=0, camera_y=0):
        dx, dy = 0.0, 0.0

        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            dy = -self.speed
        if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            dy = self.speed
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            dx = -self.speed
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            dx = self.speed

        # Diagonal normalisation
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        # Walk animation / footstep sound
        if dx != 0 or dy != 0:
            self.bob += 0.15
            self.footstep_timer -= 1
            if self.footstep_timer <= 0:
                snd_footstep.play()
                self.footstep_timer = 15

        # Mouse aiming - convert screen coords to world coords
        mx, my = pygame.mouse.get_pos()
        world_mx = mx + camera_x
        world_my = my + camera_y
        self.facing = math.atan2(world_my - self.y, world_mx - self.x)

        # Movement with wall collision (test X and Y separately)
        new_x = self.x + dx
        new_y = self.y + dy

        test_rect_x = pygame.Rect(new_x - 10, self.y - 10, 20, 20)
        test_rect_y = pygame.Rect(self.x - 10, new_y - 10, 20, 20)

        if not is_wall_at(test_rect_x, tile_map):
            self.x = new_x
        if not is_wall_at(test_rect_y, tile_map):
            self.y = new_y

        # Timers
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.invuln_timer > 0:
            self.invuln_timer -= 1

        # Flashlight battery
        if self.flashlight_on:
            self.battery -= 0.03
            if self.battery <= 0:
                self.battery = 0
                self.flashlight_on = False
        elif self.battery < 100:
            self.battery += 0.01

        # Sanity drain in darkness
        if not self.flashlight_on:
            self.sanity = max(0, self.sanity - 0.05)

        # Low-sanity hallucination trigger
        if self.sanity < 30:
            self.sanity_timer += 1
            if self.sanity_timer >= 300 and random.random() < 0.02:
                snd_sanity_low.play()
                self.sanity_timer = 0


