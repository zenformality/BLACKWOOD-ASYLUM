# ══════════════════════════════════════════════════════════════════════════════
#  utils.py — Small reusable helper functions
# ══════════════════════════════════════════════════════════════════════════════

from config import BLACK


def draw_text(surf, text, font, color, cx, cy, outline=BLACK, outline_w=2):
    """Render text with a dark outline for readability."""
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx * dx + dy * dy <= outline_w * outline_w + 1:
                s = font.render(text, True, outline)
                surf.blit(s, s.get_rect(center=(cx + dx, cy + dy)))
    s = font.render(text, True, color)
    surf.blit(s, s.get_rect(center=(cx, cy)))


def draw_text_alpha(surf, text, font, color, cx, cy, alpha):
    """Render text with a specific alpha transparency."""
    s = font.render(text, True, color)
    s.set_alpha(max(0, min(255, int(alpha))))
    surf.blit(s, s.get_rect(center=(cx, cy)))


def lerp(a, b, t):
    """Linear interpolation between a and b by factor t."""
    return a + (b - a) * t
