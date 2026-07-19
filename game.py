# ══════════════════════════════════════════════════════════════════════════════
#  game.py — Central Game class (state machine, update loop, event handling)
# ══════════════════════════════════════════════════════════════════════════════

import random
import pygame

from config import W, H, TILE, FPS
from assets import (
    snd_door, snd_pickup, snd_key, snd_locked,
    snd_scare, snd_whisper,
)
from story import STORY_NOTES
from level import create_level, check_tile_pickups, try_interact
from player import Player
from enemy import Enemy
from utils import lerp
import renderer


class Game:
    """Owns every piece of game state and drives the main loop."""

    def __init__(self, screen_surface):
        self.screen = screen_surface
        self.state = "menu"          # menu | intro | playing | reading | jumpscare | dead | win
        self.tile_map = None
        self.player = None
        self.enemies = []
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.frame = 0

        # Jumpscare
        self.scare_timer = 0
        self.scare_duration = 120
        self.death_reason = ""

        # Reading overlay
        self.reading_note = None

        # Intro sequence
        self.intro_timer = 0
        self.intro_text_idx = 0

        # Floating message
        self.message = ""
        self.message_timer = 0

        # Misc
        self.screen_shake = 0
        self.game_time = 0
        self.jumpscare_triggered = False

        # Menu particles
        self.menu_particles = self._make_menu_particles()

    # ── Menu particles ───────────────────────────────────────────────────────

    @staticmethod
    def _make_menu_particles():
        return [{
            'x': random.randint(0, W),
            'y': random.randint(0, H),
            'speed': random.uniform(0.3, 1.5),
            'size': random.randint(1, 3),
            'alpha': random.randint(30, 120),
        } for _ in range(50)]

    # ── Start / reset ────────────────────────────────────────────────────────

    def start_game(self):
        self.tile_map, spawns = create_level()

        # Find player start tile and clear it
        for y in range(len(self.tile_map)):
            for x in range(len(self.tile_map[y])):
                if self.tile_map[y][x] == 'S':
                    self.tile_map[y][x] = 0
                    self.player = Player(x * TILE + TILE // 2, y * TILE + TILE // 2)
                    break

        self.enemies = [Enemy(ex, ey, beh) for ex, ey, beh in spawns]
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.frame = 0
        self.game_time = 0
        self.jumpscare_triggered = False

        self.state = "intro"
        self.intro_timer = 0
        self.intro_text_idx = 0

    def _show_message(self, msg, duration=120):
        self.message = msg
        self.message_timer = duration

    # ── Tile interaction dispatch ─────────────────────────────────────────────

    def _handle_auto_pickups(self):
        if not self.player:
            return
        result = check_tile_pickups(self.player, self.tile_map)
        if result == "pickup_hp":
            snd_pickup.play()
            self._show_message("+30 HP")
        elif result == "pickup_bat":
            snd_pickup.play()
            self._show_message("+40 Battery")

    def _handle_interact(self):
        if not self.player:
            return
        event, data = try_interact(self.player, self.tile_map, STORY_NOTES)

        if event == "key":
            snd_key.play()
            self._show_message(f"Got {data} key!")

        elif event == "note":
            self.reading_note = data
            self.state = "reading"
            snd_whisper.play()

        elif event == "door_open":
            snd_door.play()
            self._show_message(f"{data} door unlocked!")

        elif event == "door_locked":
            snd_locked.play()
            self._show_message(f"Need {data} key!")

        elif event == "exit":
            self.state = "win"

    # ── Playing update ────────────────────────────────────────────────────────

    def _update_playing(self):
        if not self.player or not self.player.alive:
            return

        self.game_time += 1

        # Player movement
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.tile_map, self.camera_x, self.camera_y)

        # Tile pickups + interaction
        self._handle_auto_pickups()

        # Enemies
        for enemy in self.enemies:
            enemy.update(self.player, self.tile_map)

        # Sanity constant damage
        if self.player.sanity <= 0:
            self.player.take_damage(0.5)

        # Camera
        target_x = self.player.x - W // 2
        target_y = self.player.y - H // 2
        self.camera_x = lerp(self.camera_x, target_x, 0.08)
        self.camera_y = lerp(self.camera_y, target_y, 0.08)

        # Timers
        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.message_timer > 0:
            self.message_timer -= 1

        # Death
        if not self.player.alive:
            self.death_reason = "You were killed by the entity."
            self.scare_timer = 0
            self.state = "jumpscare"

        # Random scare at low sanity
        if (self.player.sanity < 20
                and random.random() < 0.002
                and not self.jumpscare_triggered):
            self.jumpscare_triggered = True
            self.scare_timer = 0
            self.death_reason = "You lost your mind..."
            self.state = "jumpscare"

    # ── Main event handler ────────────────────────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self._handle_escape()

                if event.key == pygame.K_SPACE:
                    return self._handle_space()

                if event.key == pygame.K_h and self.state == "menu":
                    self.state = "how_to_play"

                if event.key == pygame.K_e:
                    if self.state == "playing":
                        self._handle_interact()
                    elif self.state == "reading":
                        self.state = "playing"
                        self.reading_note = None

                if event.key == pygame.K_f and self.state == "playing" and self.player:
                    self.player.flashlight_on = not self.player.flashlight_on

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "menu":
                    self.start_game()
                elif self.state == "playing":
                    self._handle_interact()

        return True

    def _handle_escape(self):
        if self.state == "reading":
            self.state = "playing"
            self.reading_note = None
        elif self.state == "playing":
            self.state = "menu"
        elif self.state == "how_to_play":
            self.state = "menu"
        elif self.state in ("dead", "win", "jumpscare"):
            self.state = "menu"
        else:
            return False  # quit
        return True

    def _handle_space(self):
        if self.state == "menu":
            self.start_game()
        elif self.state == "how_to_play":
            self.state = "menu"
        elif self.state == "intro":
            self.intro_text_idx = 999  # skip to end
            self.state = "playing"
        elif self.state == "dead":
            self.start_game()
        elif self.state == "win":
            self.start_game()
        elif self.state == "playing":
            self._handle_interact()
        elif self.state == "reading":
            self.state = "playing"
            self.reading_note = None
        return True

    # ── Main update ───────────────────────────────────────────────────────────

    def _update(self):
        if self.state == "menu":
            pass

        elif self.state == "intro":
            self.intro_timer += 1
            if self.intro_timer > 90:
                self.intro_timer = 0
                self.intro_text_idx += 1
            from story import INTRO_TEXTS
            if self.intro_text_idx >= len(INTRO_TEXTS):
                self.state = "playing"

        elif self.state == "playing":
            self._update_playing()

        elif self.state == "jumpscare":
            self.scare_timer += 1
            if self.scare_timer == 1:
                snd_scare.play()
                self.screen_shake = 20
            if self.scare_timer > self.scare_duration:
                self.state = "dead"

    # ── Main draw ─────────────────────────────────────────────────────────────

    def _draw(self):
        s = self.screen
        if self.state == "menu":
            renderer.draw_menu(s, self.menu_particles)

        elif self.state == "how_to_play":
            renderer.draw_how_to_play(s)

        elif self.state == "intro":
            renderer.draw_intro(s, self.intro_text_idx, self.intro_timer)

        elif self.state in ("playing", "reading"):
            sx = random.randint(-3, 3) if self.screen_shake > 0 else 0
            sy = random.randint(-3, 3) if self.screen_shake > 0 else 0
            saved = self.camera_x, self.camera_y
            self.camera_x += sx
            self.camera_y += sy

            s.fill((0, 0, 0))
            renderer.draw_map(s, self.tile_map, self.camera_x, self.camera_y, self.frame)
            renderer.draw_player(s, self.player, self.camera_x, self.camera_y)
            for enemy in self.enemies:
                enemy.draw(s, self.camera_x, self.camera_y)
            renderer.draw_darkness(s, self.player, self.camera_x, self.camera_y)
            renderer.draw_sanity_effects(s, self.player, self.frame)
            renderer.draw_hud(s, self.player, self.message, self.message_timer, self.game_time)
            renderer.draw_interact_prompt(s, self.player, self.tile_map, self.camera_x, self.camera_y)

            self.camera_x, self.camera_y = saved

            if self.state == "reading":
                renderer.draw_reading_screen(s, self.reading_note)

        elif self.state == "jumpscare":
            s.fill((10, 0, 0))
            renderer.draw_jumpscare(s, self.scare_timer, self.scare_duration)

        elif self.state == "dead":
            renderer.draw_death_screen(s, self.death_reason, self.player)

        elif self.state == "win":
            renderer.draw_win_screen(s, self.player)

    # ── Public entry point ────────────────────────────────────────────────────

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(FPS)
            self.frame += 1

            running = self._handle_events()
            self._update()
            self._draw()

            pygame.display.flip()

        pygame.quit()
