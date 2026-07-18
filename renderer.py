# ══════════════════════════════════════════════════════════════════════════════
#  renderer.py — All drawing / rendering functions
# ══════════════════════════════════════════════════════════════════════════════

import math
import random
import pygame

from config import (
    W, H, TILE, MAP_W, MAP_H,
    BLACK, WHITE, RED, CRIMSON, GREEN, YELLOW, ORANGE, GREY,
    DARK_GREY, LIGHT_GREY, WALL_COLOR, FLOOR_COLOR, DOOR_COLOR,
    KEY_RED, KEY_BLUE, KEY_GREEN, KEY_YELLOW,
    font_huge, font_big, font_mid, font_small, font_tiny,
    font_note, font_note_b,
)
from assets import img_jumpscare, img_title_bg
from utils import draw_text, draw_text_alpha, lerp
from story import STORY_NOTES


# ══════════════════════════════════════════════════════════════════════════════
#  MAP DRAWING
# ══════════════════════════════════════════════════════════════════════════════

def draw_map(surf, tile_map, camera_x, camera_y, frame):
    """Draw only the tiles currently visible on screen."""
    start_tx = max(0, int(camera_x // TILE) - 1)
    end_tx   = min(MAP_W, int((camera_x + W) // TILE) + 2)
    start_ty = max(0, int(camera_y // TILE) - 1)
    end_ty   = min(MAP_H, int((camera_y + H) // TILE) + 2)

    for ty in range(start_ty, end_ty):
        for tx in range(start_tx, end_tx):
            tile = tile_map[ty][tx]
            sx = tx * TILE - camera_x
            sy = ty * TILE - camera_y

            if tile == 0 or tile == 'S':
                _draw_floor(surf, sx, sy, tx, ty)
            elif tile == 1:
                _draw_wall(surf, sx, sy, tx, ty)
            elif isinstance(tile, str):
                _draw_special_tile(surf, sx, sy, tile, frame)


def _draw_floor(surf, sx, sy, tx, ty):
    surf.fill(FLOOR_COLOR, (sx, sy, TILE, TILE))
    if (tx + ty) % 3 == 0:
        pygame.draw.rect(surf, (30, 30, 33), (sx + 2, sy + 2, TILE - 4, TILE - 4))
    if (tx * 7 + ty * 13) % 37 == 0:
        pygame.draw.circle(surf, (80, 0, 0), (sx + TILE // 2, sy + TILE // 2), 4)


def _draw_wall(surf, sx, sy, tx, ty):
    surf.fill(WALL_COLOR, (sx, sy, TILE, TILE))
    pygame.draw.rect(surf, (60, 60, 65), (sx + 2, sy + 2, TILE - 4, TILE - 4))
    if ty % 2 == 0:
        pygame.draw.line(surf, (40, 40, 43), (sx, sy + TILE // 2), (sx + TILE, sy + TILE // 2))
    pygame.draw.line(surf, (40, 40, 43), (sx + TILE // 2, sy), (sx + TILE // 2, sy + TILE))


def _draw_special_tile(surf, sx, sy, tile, frame):
    """Draw keys, notes, doors, pickups, exit."""
    # ── Locked door ──────────────────────────────────────────────────────
    if tile in ('R', 'B', 'G', 'Y'):
        colors = {'R': KEY_RED, 'B': KEY_BLUE, 'G': KEY_GREEN, 'Y': KEY_YELLOW}
        surf.fill(DOOR_COLOR, (sx, sy, TILE, TILE))
        surf.fill(DOOR_COLOR, (sx + 4, sy + 4, TILE - 8, TILE - 8))
        c = colors[tile]
        pygame.draw.rect(surf, c, (sx + TILE // 2 - 6, sy + TILE // 2 - 6, 12, 12))
        pygame.draw.rect(surf, c, (sx + 4, sy + TILE - 16, TILE - 8, 6))

    # ── Key ──────────────────────────────────────────────────────────────
    elif tile.startswith('k'):
        colors = {'kR': KEY_RED, 'kB': KEY_BLUE, 'kG': KEY_GREEN, 'kY': KEY_YELLOW}
        surf.fill(FLOOR_COLOR, (sx, sy, TILE, TILE))
        c = colors.get(tile, YELLOW)
        kx, ky = sx + TILE // 2, sy + TILE // 2
        pygame.draw.circle(surf, c, (kx, ky - 4), 6, 2)
        pygame.draw.line(surf, c, (kx, ky + 2), (kx, ky + 14), 3)
        pygame.draw.line(surf, c, (kx, ky + 10), (kx + 6, ky + 10), 3)
        pygame.draw.line(surf, c, (kx, ky + 14), (kx + 4, ky + 14), 3)
        glow = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        ga = int(30 + 20 * math.sin(frame * 0.05))
        pygame.draw.circle(glow, (*c, ga), (TILE // 2, TILE // 2), 20)
        surf.blit(glow, (sx, sy))

    # ── Note ─────────────────────────────────────────────────────────────
    elif tile.startswith('n'):
        surf.fill(FLOOR_COLOR, (sx, sy, TILE, TILE))
        pygame.draw.rect(surf, (200, 200, 180), (sx + 10, sy + 8, 28, 32))
        pygame.draw.rect(surf, (180, 180, 160), (sx + 10, sy + 8, 28, 32), 2)
        for i in range(3):
            pygame.draw.line(surf, (140, 140, 130),
                             (sx + 14, sy + 16 + i * 8),
                             (sx + 34, sy + 16 + i * 8))

    # ── Health pickup ────────────────────────────────────────────────────
    elif tile == 'h':
        surf.fill(FLOOR_COLOR, (sx, sy, TILE, TILE))
        pygame.draw.rect(surf, RED, (sx + 14, sy + 10, 20, 28))
        pygame.draw.rect(surf, WHITE, (sx + 20, sy + 14, 8, 20))
        pygame.draw.rect(surf, WHITE, (sx + 14, sy + 20, 20, 8))

    # ── Battery pickup ───────────────────────────────────────────────────
    elif tile == 'b':
        surf.fill(FLOOR_COLOR, (sx, sy, TILE, TILE))
        pygame.draw.rect(surf, (100, 100, 100), (sx + 14, sy + 12, 20, 24))
        pygame.draw.rect(surf, (150, 150, 150), (sx + 18, sy + 8, 12, 6))
        pygame.draw.polygon(surf, YELLOW, [
            (sx + 26, sy + 14), (sx + 20, sy + 24),
            (sx + 25, sy + 24), (sx + 22, sy + 34),
            (sx + 30, sy + 22), (sx + 25, sy + 22),
        ])

    # ── Exit ─────────────────────────────────────────────────────────────
    elif tile == 'E':
        surf.fill(FLOOR_COLOR, (sx, sy, TILE, TILE))
        pygame.draw.rect(surf, (30, 80, 30), (sx + 4, sy + 4, TILE - 8, TILE - 8))
        draw_text(surf, "EXIT", font_tiny, GREEN, sx + TILE // 2, sy + TILE // 2)


# ══════════════════════════════════════════════════════════════════════════════
#  PLAYER DRAWING
# ══════════════════════════════════════════════════════════════════════════════

def draw_player(surf, player, camera_x, camera_y):
    if not player:
        return
    sx = player.x - camera_x
    sy = player.y - camera_y

    # Hurt flash — skip every other frame
    if player.hurt_timer > 0 and player.hurt_timer % 4 < 2:
        return

    body = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.circle(body, (200, 170, 140), (12, 8), 7)    # head
    pygame.draw.rect(body, (50, 60, 100), (6, 14, 12, 10))   # torso

    if player.flashlight_on:
        fx = math.cos(player.facing) * 16
        fy = math.sin(player.facing) * 16
        glow = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 240, 180, 80), (4, 4), 4)
        body.blit(glow, (int(12 + fx - 4), int(8 + fy - 4)))

    surf.blit(body, (sx - 12, sy - 12))

    if player.flashlight_on:
        beam_len = 40
        ex = sx + math.cos(player.facing) * beam_len
        ey = sy + math.sin(player.facing) * beam_len
        pygame.draw.line(surf, (255, 240, 150, 60), (int(sx), int(sy)), (int(ex), int(ey)), 2)


# ══════════════════════════════════════════════════════════════════════════════
#  DARKNESS / LIGHTING
# ══════════════════════════════════════════════════════════════════════════════

def draw_darkness(surf, player):
    if not player:
        return

    fog = pygame.Surface((W, H), pygame.SRCALPHA)

    if player.flashlight_on:
        fog.fill((0, 0, 0, 180))
        px = int(player.x)
        py = int(player.y)
        radius = player.flashlight_radius
        pygame.draw.circle(fog, (0, 0, 0, 0), (px, py), int(radius))
        for r in range(int(radius), int(radius + 80), 5):
            a = int(180 * (r - radius) / 80)
            pygame.draw.circle(fog, (0, 0, 0, a), (px, py), r)
    else:
        fog.fill((0, 0, 0, 210))
        px = int(player.x)
        py = int(player.y)
        for r in range(60, 0, -3):
            a = int(210 * (1 - r / 60))
            pygame.draw.circle(fog, (0, 0, 0, max(0, 210 - a)), (px, py), r)

    surf.blit(fog, (0, 0))


# ══════════════════════════════════════════════════════════════════════════════
#  HUD
# ══════════════════════════════════════════════════════════════════════════════

def draw_hud(surf, player, message, message_timer, game_time):
    if not player:
        return

    bar_w, bar_h = 200, 16
    bx, by = 20, 20

    # ── HP ────────────────────────────────────────────────────────────────
    pygame.draw.rect(surf, DARK_GREY, (bx, by, bar_w, bar_h))
    hw = int(bar_w * player.hp / player.max_hp)
    hc = RED if player.hp < 30 else (200, 50, 50)
    pygame.draw.rect(surf, hc, (bx, by, hw, bar_h))
    pygame.draw.rect(surf, WHITE, (bx, by, bar_w, bar_h), 1)
    draw_text(surf, f"HP: {int(player.hp)}", font_tiny, WHITE, bx + bar_w // 2, by + bar_h // 2)

    # ── Sanity ────────────────────────────────────────────────────────────
    sy = by + bar_h + 8
    pygame.draw.rect(surf, DARK_GREY, (bx, sy, bar_w, bar_h))
    sw = int(bar_w * player.sanity / player.max_sanity)
    sc = (120, 0, 180) if player.sanity > 30 else (180, 0, 220)
    pygame.draw.rect(surf, sc, (bx, sy, sw, bar_h))
    pygame.draw.rect(surf, WHITE, (bx, sy, bar_w, bar_h), 1)
    draw_text(surf, f"Sanity: {int(player.sanity)}", font_tiny, WHITE, bx + bar_w // 2, sy + bar_h // 2)

    # ── Battery ───────────────────────────────────────────────────────────
    bat_y = sy + bar_h + 8
    pygame.draw.rect(surf, DARK_GREY, (bx, bat_y, bar_w, bar_h))
    bw = int(bar_w * player.battery / 100)
    bc = YELLOW if player.battery > 30 else ORANGE
    pygame.draw.rect(surf, bc, (bx, bat_y, bw, bar_h))
    pygame.draw.rect(surf, WHITE, (bx, bat_y, bar_w, bar_h), 1)
    bt = "ON" if player.flashlight_on else "OFF"
    draw_text(surf, f"Light: {int(player.battery)}% [{bt}]", font_tiny, WHITE, bx + bar_w // 2, bat_y + bar_h // 2)

    # ── Keys ──────────────────────────────────────────────────────────────
    key_y = bat_y + bar_h + 15
    key_cols = {'R': KEY_RED, 'B': KEY_BLUE, 'G': KEY_GREEN, 'Y': KEY_YELLOW}
    for i, (kc, color) in enumerate(key_cols.items()):
        kx = bx + i * 35
        if kc in player.keys:
            pygame.draw.rect(surf, color, (kx, key_y, 28, 20))
            pygame.draw.rect(surf, WHITE, (kx, key_y, 28, 20), 1)
            draw_text(surf, kc, font_tiny, WHITE, kx + 14, key_y + 10)
        else:
            pygame.draw.rect(surf, DARK_GREY, (kx, key_y, 28, 20))
            pygame.draw.rect(surf, GREY, (kx, key_y, 28, 20), 1)

    # ── Notes counter ─────────────────────────────────────────────────────
    draw_text(surf, f"Notes: {len(player.notes)}/{len(STORY_NOTES)}",
              font_tiny, LIGHT_GREY, W // 2, 30)

    # ── Floating message ──────────────────────────────────────────────────
    if message_timer > 0:
        alpha = min(255, message_timer * 4)
        draw_text_alpha(surf, message, font_mid, YELLOW, W // 2, H // 2 - 50, alpha)

    # ── Controls hint (fades out) ─────────────────────────────────────────
    if game_time < 300:
        alpha = min(255, max(0, (300 - game_time) * 2))
        hint = "WASD: Move | Mouse: Aim | F: Flashlight | E: Interact | ESC: Menu"
        draw_text_alpha(surf, hint, font_tiny, (200, 200, 200), W // 2, H - 40, alpha)


# ══════════════════════════════════════════════════════════════════════════════
#  SANITY / HALLUCINATION OVERLAY
# ══════════════════════════════════════════════════════════════════════════════

def draw_sanity_effects(surf, player, frame):
    if not player or player.sanity >= 50:
        return

    intensity = (50 - player.sanity) / 50

    # Red border pulse
    border = pygame.Surface((W, H), pygame.SRCALPHA)
    pulse = int(50 * intensity * (0.5 + 0.5 * math.sin(frame * 0.1)))
    ba = min(200, pulse)
    for rect in [(0, 0, W, 20), (0, H - 20, W, 20), (0, 0, 20, H), (W - 20, 0, 20, H)]:
        pygame.draw.rect(border, (80, 0, 0, ba), rect)
    surf.blit(border, (0, 0))

    # Random flicker
    if random.random() < intensity * 0.05:
        flicker = pygame.Surface((W, H), pygame.SRCALPHA)
        flicker.fill((0, 0, 0, random.randint(50, 150)))
        surf.blit(flicker, (0, 0))

    # Glitch lines
    if random.random() < intensity * 0.1:
        ly = random.randint(0, H)
        pygame.draw.line(surf, (200, 0, 0), (0, ly), (W, ly), 1)


# ══════════════════════════════════════════════════════════════════════════════
#  JUMPSCARE
# ══════════════════════════════════════════════════════════════════════════════

def draw_jumpscare(surf, scare_timer, scare_duration):
    from story import SCARE_TEXTS

    frac = min(1.0, scare_timer / 10)

    # Background flash
    if scare_timer < 5:
        surf.fill((255, 255, 255))
    elif scare_timer < 15:
        surf.fill((200, 0, 0))
    else:
        surf.fill((20, 0, 0))

    # Use real image if available
    if img_jumpscare:
        img = pygame.transform.scale(img_jumpscare, (W, H))
        img.set_alpha(int(frac * 255))
        surf.blit(img, (0, 0))
    elif scare_timer >= 5:
        _draw_procedural_monster(surf, frac)

    # Flickering text
    if scare_timer > 30:
        txt = random.choice(SCARE_TEXTS)
        draw_text(surf, txt, font_big, CRIMSON, W // 2, H - 100)

    # Glitch lines
    if scare_timer > 10:
        for _ in range(5):
            gy = random.randint(0, H)
            gh = random.randint(2, 8)
            pygame.draw.rect(surf, (255, 0, 0, 100), (0, gy, W, gh))


def _draw_procedural_monster(surf, frac):
    """Fallback monster face when no jumpscare.png exists."""
    face = pygame.Surface((W, H), pygame.SRCALPHA)
    eye_size = int(80 * frac)

    for ex, ey in [(W // 2 - 120, H // 2 - 40), (W // 2 + 120, H // 2 - 40)]:
        pygame.draw.ellipse(face, (200, 200, 200, 200),
                            (ex - eye_size // 2, ey - eye_size // 3, eye_size, int(eye_size * 0.7)))
        pupil = int(eye_size * 0.4)
        pygame.draw.circle(face, (180, 0, 0), (ex, ey), pupil)
        pygame.draw.circle(face, BLACK, (ex, ey), pupil - 5)
        pygame.draw.circle(face, (255, 0, 0), (ex + 10, ey - 5), 3)

    mouth_y = H // 2 + 60
    mouth_w = int(200 * frac)
    pygame.draw.ellipse(face, (60, 0, 0, 200),
                        (W // 2 - mouth_w // 2, mouth_y - 20, mouth_w, 60))
    for i in range(int(mouth_w / 20)):
        tx = W // 2 - mouth_w // 2 + i * 20 + 5
        pygame.draw.polygon(face, (220, 220, 200, 200),
                            [(tx, mouth_y - 15), (tx + 10, mouth_y - 15), (tx + 5, mouth_y + 5)])
        pygame.draw.polygon(face, (220, 220, 200, 200),
                            [(tx, mouth_y + 30), (tx + 10, mouth_y + 30), (tx + 5, mouth_y + 15)])

    surf.blit(face, (0, 0))


# ══════════════════════════════════════════════════════════════════════════════
#  DEATH SCREEN
# ══════════════════════════════════════════════════════════════════════════════

def draw_death_screen(surf, death_reason, player):
    surf.fill((10, 0, 0))

    for i in range(20):
        x = (i * 57 + 23) % W
        h = random.randint(50, 200)
        a = random.randint(60, 150)
        drip = pygame.Surface((6, h), pygame.SRCALPHA)
        drip.fill((139, 0, 0, a))
        surf.blit(drip, (x, 0))

    draw_text(surf, "YOU DIED", font_huge, CRIMSON, W // 2, H // 2 - 80)
    draw_text(surf, death_reason, font_mid, LIGHT_GREY, W // 2, H // 2)
    notes = len(player.notes) if player else 0
    draw_text(surf, f"Notes found: {notes}/{len(STORY_NOTES)}", font_small, LIGHT_GREY, W // 2, H // 2 + 50)
    draw_text(surf, "Press SPACE to retry", font_mid, WHITE, W // 2, H // 2 + 120)
    draw_text(surf, "Press ESC for menu", font_small, GREY, W // 2, H // 2 + 160)


# ══════════════════════════════════════════════════════════════════════════════
#  WIN SCREEN
# ══════════════════════════════════════════════════════════════════════════════

def draw_win_screen(surf, player):
    surf.fill((0, 10, 0))

    for i in range(50):
        sx = (i * 97 + 31) % W
        sy = (i * 63 + 17) % H
        pygame.draw.circle(surf, WHITE, (sx, sy), 1)

    draw_text(surf, "ESCAPED", font_huge, GREEN, W // 2, H // 2 - 100)
    draw_text(surf, "You found your way out of Blackwood Asylum.",
              font_mid, LIGHT_GREY, W // 2, H // 2 - 20)

    notes = len(player.notes) if player else 0
    if notes >= len(STORY_NOTES):
        draw_text(surf, "You found ALL the notes. The truth is revealed.",
                  font_small, YELLOW, W // 2, H // 2 + 30)
    else:
        draw_text(surf, f"Notes found: {notes}/{len(STORY_NOTES)}",
                  font_small, LIGHT_GREY, W // 2, H // 2 + 30)
        draw_text(surf, "Some secrets remain hidden...",
                  font_small, GREY, W // 2, H // 2 + 60)

    draw_text(surf, "Press SPACE to play again", font_mid, WHITE, W // 2, H // 2 + 130)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════════════════

def draw_menu(surf, particles):
    surf.fill((5, 0, 8))

    # Background image (if loaded)
    if img_title_bg:
        bg = pygame.transform.scale(img_title_bg, (W, H))
        bg.set_alpha(80)
        surf.blit(bg, (0, 0))

    # Floating ember particles
    for p in particles:
        p['y'] -= p['speed']
        if p['y'] < 0:
            p['y'] = H
            p['x'] = random.randint(0, W)
        glow = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (120, 30, 30, p['alpha']), (p['size'], p['size']), p['size'])
        surf.blit(glow, (int(p['x']), int(p['y'])))

    # Title with flicker
    flicker = 255 if random.random() > 0.05 else random.randint(100, 200)
    ty = H // 3
    draw_text_alpha(surf, "BLACKWOOD", font_huge, (180, 30, 30), W // 2, ty, flicker)
    draw_text_alpha(surf, "ASYLUM", font_huge, (160, 20, 20), W // 2, ty + 80, flicker)

    t = pygame.time.get_ticks()
    sub_alpha = int(150 + 80 * math.sin(t / 1000))
    draw_text_alpha(surf, "Some doors should never be opened.",
                    font_small, (150, 80, 80), W // 2, ty + 140, sub_alpha)

    # Menu options
    my = H // 2 + 40
    draw_text(surf, "[ SPACE ]  Start Game", font_mid, WHITE, W // 2, my)
    draw_text(surf, "[ H ]  How to Play", font_mid, (180, 180, 180), W // 2, my + 50)
    draw_text(surf, "[ ESC ]  Quit", font_small, GREY, W // 2, my + 100)
    draw_text(surf, "A game of darkness and dread", font_tiny, (80, 50, 50), W // 2, H - 50)


# ══════════════════════════════════════════════════════════════════════════════
#  HOW TO PLAY SCREEN
# ══════════════════════════════════════════════════════════════════════════════

def draw_how_to_play(surf):
    from story import HOW_TO_PLAY

    surf.fill((5, 0, 8))
    y = 80
    draw_text(surf, "HOW TO PLAY", font_big, RED, W // 2, y)
    y += 80
    for key, desc in HOW_TO_PLAY:
        if key:
            draw_text(surf, f"{key} — {desc}", font_small, WHITE, W // 2, y)
        elif desc:
            draw_text(surf, desc, font_small, (180, 140, 140), W // 2, y)
        y += 32
    draw_text(surf, "Press any key to return", font_small, GREY, W // 2, H - 50)


# ══════════════════════════════════════════════════════════════════════════════
#  NOTE READING OVERLAY
# ══════════════════════════════════════════════════════════════════════════════

def draw_reading_screen(surf, note):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surf.blit(overlay, (0, 0))

    if not note:
        return

    pw, ph = 600, 400
    px = (W - pw) // 2
    py = (H - ph) // 2

    paper = pygame.Surface((pw, ph), pygame.SRCALPHA)
    paper.fill((220, 210, 190, 240))

    title = font_note_b.render(note["title"], True, (40, 30, 20))
    paper.blit(title, (30, 20))
    pygame.draw.line(paper, (150, 140, 120), (30, 55), (pw - 30, 55))

    for i, line in enumerate(note["text"].split("\n")):
        txt = font_note.render(line, True, (50, 40, 30))
        paper.blit(txt, (30, 70 + i * 22))

    surf.blit(paper, (px, py))
    draw_text(surf, "Press E or SPACE to close", font_small, WHITE, W // 2, py + ph + 30)


# ══════════════════════════════════════════════════════════════════════════════
#  INTRO SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

def draw_intro(surf, intro_idx, intro_timer):
    from story import INTRO_TEXTS

    surf.fill(BLACK)

    if intro_idx < len(INTRO_TEXTS):
        text = INTRO_TEXTS[intro_idx]
        if text:
            draw_text(surf, text, font_mid, WHITE, W // 2, H // 2)

    draw_text(surf, "Press SPACE to skip", font_tiny, GREY, W // 2, H - 40)
