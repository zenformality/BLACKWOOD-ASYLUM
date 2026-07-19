# ══════════════════════════════════════════════════════════════════════════════
#  assets.py — Procedural sound generation + asset loading from disk
# ══════════════════════════════════════════════════════════════════════════════

import math
import random
import os
import pygame

from config import ASSET_DIR


# ── Procedural sound generators ─────────────────────────────────────────────

def generate_beep(freq=440, duration_ms=200, volume=0.3):
    """Generate a simple sine-wave beep sound."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n_samples * 2)  # 16-bit mono
    for i in range(n_samples):
        t = i / sample_rate
        fade = max(0, 1.0 - (i / n_samples) * 2)
        val = int(32767 * volume * fade * math.sin(2 * math.pi * freq * t))
        val = max(-32768, min(32767, val))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))


def generate_noise(duration_ms=300, volume=0.15):
    """Generate static noise."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n_samples * 2)
    for i in range(n_samples):
        fade = max(0, 1.0 - (i / n_samples))
        val = int(32767 * volume * fade * (random.random() * 2 - 1))
        val = max(-32768, min(32767, val))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))


# ── Load from disk (with fallback to procedural) ────────────────────────────

def _try_load_sound(filename):
    """Try to load a .wav / .mp3 / .ogg from assets/sounds/. Falls back to None."""
    base, _ = os.path.splitext(filename)
    for ext in ('.mp3', '.wav', '.ogg'):
        path = os.path.join(ASSET_DIR, 'sounds', base + ext)
        if os.path.isfile(path):
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                pass
    return None


def _try_load_image(filename):
    """Try to load a .png from assets/images/. Falls back to None."""
    path = os.path.join(ASSET_DIR, "images", filename)
    if os.path.isfile(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception:
            pass
    return None


# ── Sound registry ──────────────────────────────────────────────────────────
# After init(), use these:  snd.play()

snd_footstep   = None
snd_door       = None
snd_pickup     = None
snd_key        = None
snd_hurt       = None
snd_scare      = None
snd_whisper    = None
snd_heartbeat  = None
snd_locked     = None
snd_sanity_low = None


def init_sounds():
    """Generate or load every sound used by the game."""
    global snd_footstep, snd_door, snd_pickup, snd_key, snd_hurt
    global snd_scare, snd_whisper, snd_heartbeat, snd_locked, snd_sanity_low

    print("Generating / loading sounds...")

    snd_footstep   = _try_load_sound("footsteps.mp3")   or generate_beep(80, 60, 0.08)
    snd_door       = _try_load_sound("door_open.mp3")    or generate_beep(150, 400, 0.15)
    snd_pickup     = _try_load_sound("pickup.mp3")       or generate_beep(800, 150, 0.2)
    snd_key        = _try_load_sound("key_collect.mp3")  or generate_beep(1200, 200, 0.25)
    snd_hurt       = _try_load_sound("hurt.mp3")         or generate_beep(100, 300, 0.3)
    snd_scare      = _try_load_sound("scare.mp3")        or generate_noise(600, 0.5)
    snd_whisper    = _try_load_sound("whisper.mp3")      or generate_noise(1500, 0.08)
    snd_heartbeat  = _try_load_sound("heartbeat.mp3")    or generate_beep(40, 100, 0.2)
    snd_locked     = _try_load_sound("locked-door.mp3")  or generate_beep(200, 300, 0.2)
    snd_sanity_low = _try_load_sound("ambient.mp3")      or generate_noise(2000, 0.12)

    print("Sounds ready!")


# ── Image registry ──────────────────────────────────────────────────────────
# Populated by init_images(). None means "use procedural fallback".

img_jumpscare = None
img_title_bg  = None

img_player = None
img_enemy  = None
img_health = None
img_battery = None
img_note   = None
img_key_red = None
img_key_blue = None
img_key_green = None
img_key_yellow = None


def init_images():
    """Load optional images. Returns nothing — check the globals."""
    global img_jumpscare, img_title_bg
    global img_player, img_enemy, img_health, img_battery, img_note
    global img_key_red, img_key_blue, img_key_green, img_key_yellow

    print("Loading images...")

    img_jumpscare = _try_load_image("jumpscare.png")
    img_title_bg  = _try_load_image("title_bg.png")
    img_player    = _try_load_image("player.png")
    img_enemy     = _try_load_image("enemy.png")
    img_health    = _try_load_image("health.png")
    img_battery   = _try_load_image("battery.png")
    img_note      = _try_load_image("note.png")
    img_key_red   = _try_load_image("key_red.png")
    img_key_blue  = _try_load_image("key_blue.png")
    img_key_green = _try_load_image("key_green.png")
    img_key_yellow= _try_load_image("key_yellow.png")

    for name, img in [
        ("jumpscare.png", img_jumpscare),
        ("title_bg.png",  img_title_bg),
        ("player.png",    img_player),
        ("enemy.png",     img_enemy),
        ("health.png",    img_health),
        ("battery.png",   img_battery),
        ("note.png",      img_note),
        ("key_red.png",   img_key_red),
        ("key_blue.png",  img_key_blue),
        ("key_green.png", img_key_green),
        ("key_yellow.png",img_key_yellow),
    ]:
        if img:
            print(f"  + {name} loaded")
        else:
            print(f"  - {name} not found (using procedural)")
