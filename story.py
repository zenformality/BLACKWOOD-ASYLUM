# ══════════════════════════════════════════════════════════════════════════════
#  story.py — All story notes, lore text, and narrative content
# ══════════════════════════════════════════════════════════════════════════════

# ── Scattered notes the player finds throughout the asylum ───────────────────
STORY_NOTES = {
    "note1": {
        "title": "Dr. Harrow's Journal — Entry 1",
        "text": (
            "September 12, 1987\n"
            "\n"
            "The patients are responding to the new treatment.\n"
            "Something in their eyes has changed... they see\n"
            "things we cannot. Dr. Webb thinks we should stop.\n"
            "He doesn't understand. We are CLOSE to breakthrough.\n"
            "\n"
            "The whispers are getting louder."
        ),
    },
    "note2": {
        "title": "Emergency Memo",
        "text": (
            "TO ALL STAFF:\n"
            "\n"
            "Ward C is now OFF LIMITS. Anyone entering without\n"
            "Level 3 clearance will face immediate termination.\n"
            "The sounds from below are NOT patients screaming.\n"
            "Do NOT investigate.\n"
            "\n"
            "\u2014 Director Ashworth"
        ),
    },
    "note3": {
        "title": "Dr. Harrow's Journal \u2014 Entry 7",
        "text": (
            "October 3rd, 1987\n"
            "\n"
            "Patient 63 spoke to me today. Not with words.\n"
            "It showed me a place \u2014 a place between walls,\n"
            "between breaths. I saw something moving in the\n"
            "darkness. It has no name. It has no face.\n"
            "\n"
            "But it knows mine."
        ),
    },
    "note4": {
        "title": "Scrawled on the wall",
        "text": (
            "IT LIVES IN THE DARK\n"
            "IT LIVES IN THE DARK\n"
            "IT LIVES IN THE D- oh god\n"
            "don't turn around\n"
            "don't turn around\n"
            "DON'T TURN AROUND"
        ),
    },
    "note5": {
        "title": "Final Transmission \u2014 Officer Davis",
        "text": (
            "Dispatch, this is Davis. I'm on floor 2.\n"
            "Something... something got Kowalski. He was\n"
            "right behind me and then he just... wasn't.\n"
            "\n"
            "There's a thing here. It moves when you\n"
            "don't look. God help me, it's RIGHT BEHIND\n"
            "\n"
            "[TRANSMISSION ENDS]"
        ),
    },
}

# ── Intro sequence text ──────────────────────────────────────────────────────
INTRO_TEXTS = [
    "Blackwood Asylum...",
    "Closed since 1987.",
    "",
    "Your partner, Detective Kowalski,",
    "went missing here three days ago.",
    "",
    "You are Detective Morgan.",
    "You came here to find him.",
    "",
    "You should not have come.",
]

# ── Jumpscare flicker text ──────────────────────────────────────────────────
SCARE_TEXTS = [
    "DON'T LOOK AWAY",
    "I SEE YOU",
    "YOU CAN'T ESCAPE",
    "THERE IS NO EXIT",
    "JOIN US",
]

# ── How to play instructions ────────────────────────────────────────────────
HOW_TO_PLAY = [
    ("WASD / Arrow Keys", "Move"),
    ("Mouse", "Aim your flashlight"),
    ("F", "Toggle flashlight"),
    ("E / Space", "Interact (keys, notes, doors)"),
    ("ESC", "Pause / Menu"),
    ("", ""),
    ("OBJECTIVE:", ""),
    ("", "Find the colored keys to unlock doors."),
    ("", "Read notes to uncover the asylum's dark story."),
    ("", "Find the EXIT to escape alive."),
    ("", ""),
    ("WATCH OUT FOR:", ""),
    ("", "An entity lurks in the darkness."),
    ("", "Keep your flashlight on to hold it back."),
    ("", "Lose all sanity and the darkness consumes you."),
]
