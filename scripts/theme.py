"""Shared palette and fonts for the generated SVGs (navy / cream / coral)."""

NAVY = "#14213D"
CREAM = "#F4EDE0"
CORAL = "#FF6B5B"
AMBER = "#F2B84B"

THEMES = {
    "light": {
        "bg": CREAM,
        "panel": "#FFFBF4",
        "fg": NAVY,
        "muted": "#5B6478",
        "line": "#D3CCBF",
        "accent": CORAL,
        "series": [CORAL, NAVY, AMBER, "#3E8E7E", "#8A7FB8", "#B9B2A6"],
    },
    "dark": {
        "bg": NAVY,
        "panel": "#1B2A4A",
        "fg": CREAM,
        "muted": "#A9B1C4",
        "line": "#2E3D60",
        "accent": CORAL,
        "series": [CORAL, CREAM, AMBER, "#5FB3A1", "#A89BD6", "#5A6478"],
    },
}

SERIF = "Fraunces, Georgia, 'Times New Roman', serif"
SANS = "'Plus Jakarta Sans', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def esc(s) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
