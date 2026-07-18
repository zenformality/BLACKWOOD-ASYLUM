# BLACKWOOD ASYLUM
### A Top-Down Horror Survival Game

---

## STORY

> *"Blackwood Asylum... Closed since 1987.*
> 
> *Your partner, Detective Kowalski, went missing here three days ago.*
> 
> *You are Detective Morgan. You came here to find him.*
> 
> *You should not have come."*

Explore the abandoned Blackwood asylum. Find colored keys to unlock doors.
Read scattered notes to uncover the dark truth behind the asylum's closure.
An entity stalks the hallways — it moves in the dark.

**Can you escape alive?**

---

## CONTROLS

| Key | Action |
|-----|--------|
| WASD / Arrow Keys | Move |
| Mouse | Aim flashlight |
| F | Toggle flashlight on/off |
| E / Space | Interact (pick up keys, read notes, open doors) |
| ESC | Menu / Back |

---

## FILE STRUCTURE

```
horror/
  main.py        ← Entry point (run this)
  config.py      ← Window size, colors, fonts
  assets.py      ← Sound generation + asset loading
  story.py       ← Story notes, lore text
  utils.py       ← Drawing helpers (draw_text, lerp)
  level.py       ← Map generation, tile queries
  player.py      ← Player class
  enemy.py       ← Shadow entity AI
  renderer.py    ← All rendering / drawing functions
  game.py        ← Game class (state machine, main loop)
  README.md      ← This file
  assets/
    images/      ← Drop your images here
    sounds/      ← Drop your sounds here
```

---

## HOW TO RUN

```bash
cd horror
py main.py
```

Requires: **Python 3.x + pygame**

```bash
py -m pip install pygame
```

---

## IMAGES TO PROVIDE

Drop these into `horror/assets/images/`:

| Filename | Size | Description |
|----------|------|-------------|
| `jumpscare.png` | Any (stretched to screen) | **Scary face shown on death**. Full-screen horror face. Transparent background works best. |
| `title_bg.png` | 1024×768 | **Main menu background**. Dark, atmospheric image of the asylum. Displayed behind title text. |

### Optional extras (not yet wired but ready to add)

| Filename | Description |
|----------|-------------|
| `player.png` | Player character sprite (replace procedural circle+rect) |
| `enemy.png` | Shadow entity sprite (replace procedural dark figure) |
| `key_red.png` | Red key pickup icon (32×32) |
| `key_blue.png` | Blue key pickup icon (32×32) |
| `key_green.png` | Green key pickup icon (32×32) |
| `key_yellow.png` | Yellow key pickup icon (32×32) |
| `note.png` | Note/paper pickup icon (32×32) |
| `health.png` | Health pickup icon (32×32) |
| `battery.png` | Battery pickup icon (32×32) |

---

## SOUNDS TO PROVIDE

Drop these into `horror/assets/sounds/`:

| Filename | Format | Description |
|----------|--------|-------------|
| `jumpscare.wav` | WAV | **Loud scary sound on death** |
| `footsteps.wav` | WAV | Player walking sound |
| `door_open.wav` | WAV | Door unlocking |
| `pickup.wav` | WAV | Generic item pickup |
| `key_collect.wav` | WAV | Picking up a key |
| `hurt.wav` | WAV | Player taking damage |
| `whisper.wav` | WAV | Reading a note |
| `heartbeat.wav` | WAV | Low sanity heartbeat |
| `locked_door.wav` | WAV | Trying a locked door |
| `ambient.wav` | WAV | Background ambiance |

> **The game runs without ANY external assets.**
> All graphics are procedurally drawn, all sounds are synthesized.
> Adding real assets will enhance the experience.

---

## OBJECTIVE

1. Find the **4 colored keys** (Red, Blue, Green, Yellow) to unlock matching doors
2. Read the **5 notes** scattered throughout to learn the full story
3. Find the **EXIT** and escape alive
4. Watch your **sanity** and **battery**!

---

## STORY NOTES (5 total)

1. **Dr. Harrow's Journal — Entry 1**: The experiment begins
2. **Emergency Memo**: Ward C is off limits
3. **Dr. Harrow's Journal — Entry 7**: Patient 63 reveals something terrible
4. **Scrawled on the wall**: A desperate warning
5. **Final Transmission — Officer Davis**: The last radio call

Find all 5 for the complete story.

---

## ASYLUM MAP

```
                    ┌─────────┐
                    │  NORTH  │  ← Red key here
                    │  WING   │
                    └────┬────┘
                         │ (Red door)
┌──────────┐       ┌─────┴──────┐       ┌──────────┐       ┌──────────┐
│  SECRET  │       │  MAIN HALL │───────│  EAST    │───────│  FAR     │
│  ROOM    │       │            │       │  WING    │       │  EAST    │
│ (Grn key)│       │            │       │          │       │ (Blue    │
└──────────┘       └─────┬──────┘       └──────────┘       │  door)   │
                         │ (Grn door)                      └────┬─────┘
┌──────────┐       ┌─────┴──────┐                               │
│ ENTRANCE │───────│            │       ┌──────────┐       ┌────┴─────┐
│ (START)  │       │            │       │ BASEMENT │       │ EXIT     │
└──────────┘       └────────────┘       │(Yel key) │       │ ROOM     │
                                        └──────────┘       └──────────┘
```

---

*Made with Pygame | All content procedurally generated*
