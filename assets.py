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
    """Try to load a .wav / .mp3 from assets/sounds/. Falls back to None."""
    path = os.path.join(ASSET_DIR, "sounds", filename)
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

    snd_footstep   = _try_load_sound("footsteps.wav")   or generate_beep(80, 60, 0.08)
    snd_door       = _try_load_sound("door_open.wav")    or generate_beep(150, 400, 0.15)
    snd_pickup     = _try_load_sound("pickup.wav")       or generate_beep(800, 150, 0.2)
    snd_key        = _try_load_sound("key_collect.wav")  or generate_beep(1200, 200, 0.25)
    snd_hurt       = _try_load_sound("hurt.wav")         or generate_beep(100, 300, 0.3)
    snd_scare      = _try_load_sound("jumpscare.wav")    or generate_noise(600, 0.5)
    snd_whisper    = _try_load_sound("whisper.wav")      or generate_noise(1500, 0.08)
    snd_heartbeat  = _try_load_sound("heartbeat.wav")    or generate_beep(40, 100, 0.2)
    snd_locked     = _try_load_sound("locked_door.wav")  or generate_beep(200, 300, 0.2)
    snd_sanity_low = _try_load_sound("ambient.wav")      or generate_noise(2000, 0.12)

    print("Sounds ready!")


# ── Image registry ──────────────────────────────────────────────────────────
# Populated by init_images(). None means "use procedural fallback".

img_jumpscare = None
img_title_bg  = None


def init_images():
    """Load optional images. Returns nothing — check the globals."""
    global img_jumpscare, img_title_bg

    print("Loading images...")

    img_jumpscare = _try_load_image("jumpscare.png")
    img_title_bg  = _try_load_image("title_bg.png")

    if img_jumpscare:
        print("  + jumpscare.png loaded")
    else:
        print("  - jumpscare.png not found (using procedural)")

    if img_title_bg:
        print("  + title_bg.png loaded")
    else:
        print("  - title_bg.png not found (using procedural)")
