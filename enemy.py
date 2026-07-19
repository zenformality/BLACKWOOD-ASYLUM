# ══════════════════════════════════════════════════════════════════════════════
#  enemy.py — Shadow entity that stalks the asylum
# ══════════════════════════════════════════════════════════════════════════════

import math
import random
import pygame

from config import MAP_W, MAP_H, TILE
from assets import img_enemy


class Enemy:
    """
    A shadow creature with glowing red eyes.
    States:
      patrol  – wander between random waypoints
      chase   – sprint toward the player
      freeze  – held still by the player's flashlight
    """

    def __init__(self, tile_x, tile_y, behaviour="patrol"):
        self.x = float(tile_x * TILE + TILE // 2)
        self.y = float(tile_y * TILE + TILE // 2)
        self.speed = 1.8
        self.chase_speed = 3.2
        self.behaviour = behaviour
        self.state = "patrol"

        # Senses
        self.sight_range = 250
        self.attack_range = 35
        self.attack_damage = 15
        self.attack_cooldown = 0
        self.attack_rate = 60

        # Patrol waypoints (generated around spawn)
        self.patrol_points = []
        self.patrol_idx = 0
        self._generate_patrol()

        # Visuals
        self.eye_glow = 0.0
        self.eye_dir = 0.0
        self.body_phase = 0.0
        self.flicker_timer = 0
        self.flicker_visible = True

    # ── Patrol generation ────────────────────────────────────────────────────

    def _generate_patrol(self):
        cx, cy = self.x, self.y
        for _ in range(4):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(80, 180)
            self.patrol_points.append((
                cx + math.cos(angle) * dist,
                cy + math.sin(angle) * dist,
            ))

    # ── Line-of-sight ────────────────────────────────────────────────────────

    def can_see_player(self, player, tile_map):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > self.sight_range:
            return False

        steps = int(dist / 10)
        for i in range(steps):
            t = i / max(steps, 1)
            cx = self.x + dx * t
            cy = self.y + dy * t
            tx = int(cx // TILE)
            ty = int(cy // TILE)
            if 0 <= tx < MAP_W and 0 <= ty < MAP_H:
                tile = tile_map[ty][tx]
                if tile == 1 or (isinstance(tile, str) and tile in ('R', 'B', 'G', 'Y')):
                    return False
        return True

    # ── Update ───────────────────────────────────────────────────────────────

    def update(self, player, tile_map):
        self.body_phase += 0.05
        self.eye_glow = 0.5 + 0.5 * math.sin(self.body_phase * 3)

        # Flicker visual
        self.flicker_timer += 1
        if self.flicker_timer > 120:
            self.flicker_timer = 0
            self.flicker_visible = True
        elif self.flicker_timer > 115:
            self.flicker_visible = random.random() > 0.5
        else:
            self.flicker_visible = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Flashlight stun — entity freezes when the beam hits it (highest priority)
        dist = math.hypot(player.x - self.x, player.y - self.y)
        if player.flashlight_on and dist < player.flashlight_radius * 0.85:
            angle_to_enemy = math.atan2(self.y - player.y, self.x - player.x)
            angle_diff = abs(angle_to_enemy - player.facing)
            while angle_diff > math.pi:
                angle_diff = abs(angle_diff - 2 * math.pi)
            if angle_diff < 0.6:  # ~34 degree cone
                self.state = "freeze"
                print(f"FLASHLIGHT FREEZE: dist={dist:.0f}, angle={angle_diff:.2f}")
                return
        elif self.state == "freeze":
            self.state = "patrol"

        can_see = self.can_see_player(player, tile_map)

        if can_see:
            self.state = "chase"
        elif self.state == "chase":
            self.state = "patrol"

        # ── Movement ─────────────────────────────────────────────────────────
        if self.state == "chase":
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                nx, ny = dx / dist, dy / dist
                self.x += nx * self.chase_speed
                self.y += ny * self.chase_speed

            if dist < self.attack_range and self.attack_cooldown <= 0:
                player.take_damage(self.attack_damage)
                self.attack_cooldown = self.attack_rate

            if dist < 300:
                player.sanity = max(0, player.sanity - 0.15)

            self.eye_dir = math.atan2(dy, dx)

        elif self.state == "patrol":
            if self.patrol_points:
                tx, ty = self.patrol_points[self.patrol_idx]
                dx = tx - self.x
                dy = ty - self.y
                dist = math.hypot(dx, dy)
                if dist < 10:
                    self.patrol_idx = (self.patrol_idx + 1) % len(self.patrol_points)
                else:
                    nx, ny = dx / dist, dy / dist
                    self.x += nx * self.speed
                    self.y += ny * self.speed
                    self.eye_dir = math.atan2(dy, dx)

    # ── Drawing ──────────────────────────────────────────────────────────────

    def draw(self, surf, camera_x, camera_y):
        if not self.flicker_visible:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        # Use enemy image if available
        if img_enemy:
            img = pygame.transform.scale(img_enemy, (80, 96))
            surf.blit(img, (sx - 40, sy - 48))
        else:
            # Fallback procedural drawing
            body = pygame.Surface((80, 96), pygame.SRCALPHA)
            pygame.draw.ellipse(body, (15, 15, 18), (10, 0, 60, 80))
            pygame.draw.ellipse(body, (10, 10, 12), (18, 16, 44, 48))

            # Glowing red eyes
            ex = 40 + math.cos(self.eye_dir) * 6
            ey = 28
            glow = int(200 * self.eye_glow)
            pygame.draw.circle(body, (glow, 20, 20), (int(ex - 10), int(ey)), 7)
            pygame.draw.circle(body, (glow, 20, 20), (int(ex + 10), int(ey)), 7)
            pygame.draw.circle(body, (255, 50, 50), (int(ex - 10), int(ey)), 3)
            pygame.draw.circle(body, (255, 50, 50), (int(ex + 10), int(ey)), 3)

            surf.blit(body, (sx - 40, sy - 48))

            # Under-glow
            glow_surf = pygame.Surface((90, 30), pygame.SRCALPHA)
            glow_alpha = int(40 * self.eye_glow)
            pygame.draw.ellipse(glow_surf, (200, 0, 0, glow_alpha), (0, 0, 90, 30))
            surf.blit(glow_surf, (sx - 45, sy + 30))
