"""Draw the animated profile header: name on the left, a small neural net
running a forward pass on the right. Writes assets/header-{light,dark}.svg.

Run once after editing the text below:  python scripts/make_header.py
"""

import random
from pathlib import Path

from theme import MONO, SANS, SERIF, THEMES, esc

W, H = 1200, 320
ROOT = Path(__file__).resolve().parent.parent

EYEBROW = "OPEN SOURCE × AI/ML"
NAME = "Pranav Singh"
TAGLINE = [
    "I build AI/ML in the open and fix bugs upstream:",
    "agent memory, research agents and graph models.",
]
CHIPS = ["open-source", "agents", "memory", "gnns", "tokenizers", "evals"]
INPUTS = ["issues", "papers", "data"]
OUTPUTS = ["PRs", "ship"]

LAYERS = [3, 5, 5, 2]
LAYER_X = [820, 915, 1010, 1105]
CY, GAP = 168, 46
PERIOD = 3.2  # seconds for one forward pass


def node_positions():
    return [
        [(x, CY + (i - (n - 1) / 2) * GAP) for i in range(n)]
        for x, n in zip(LAYER_X, LAYERS)
    ]


def build(mode: str) -> str:
    t = THEMES[mode]
    rng = random.Random(7)
    nodes = node_positions()
    step = PERIOD / (len(LAYERS) + 1)

    edges, pulses = [], []
    for li in range(len(LAYERS) - 1):
        for (x1, y1) in nodes[li]:
            for (x2, y2) in nodes[li + 1]:
                d = f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}"
                edges.append(f'<path d="{d}" class="edge"/>')
                if rng.random() < 0.45:
                    delay = li * step + 0.1 + rng.random() * 0.2
                    pulses.append(
                        f'<path d="{d}" pathLength="1" class="pulse" '
                        f'style="animation-delay:{delay:.2f}s"/>'
                    )

    circles = []
    for li, layer in enumerate(nodes):
        delay = li * step + (0.25 if li else 0)
        for (x, y) in layer:
            circles.append(
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" class="node"/>'
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" class="fire" '
                f'style="animation-delay:{delay:.2f}s"/>'
            )

    labels = []
    for (x, y), name in zip(nodes[0], INPUTS):
        labels.append(f'<text x="{x - 20:.0f}" y="{y + 4:.0f}" text-anchor="end" class="io">{esc(name)}</text>')
    for (x, y), name in zip(nodes[-1], OUTPUTS):
        labels.append(f'<text x="{x + 20:.0f}" y="{y + 4:.0f}" class="io">{esc(name)}</text>')

    tagline = "".join(
        f'<text x="56" y="{218 + i * 28}" class="tag">{esc(line)}</text>' for i, line in enumerate(TAGLINE)
    )

    chips, cx = [], 56
    for c in CHIPS:
        w = 18 + len(c) * 8
        chips.append(
            f'<rect x="{cx}" y="268" width="{w}" height="24" rx="12" class="chip"/>'
            f'<text x="{cx + w / 2:.0f}" y="284" text-anchor="middle" class="chipt">{esc(c)}</text>'
        )
        cx += w + 8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Pranav Singh, AI/ML engineer">
<title>Pranav Singh, AI/ML engineer</title>
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.2" fill="{t['fg']}" opacity="0.10"/>
  </pattern>
  <radialGradient id="glow" cx="0.78" cy="0.5" r="0.45">
    <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.16"/>
    <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>
  .edge {{ stroke:{t['fg']}; stroke-opacity:.13; stroke-width:1.2; fill:none }}
  .pulse {{ stroke:{t['accent']}; stroke-width:2.6; stroke-linecap:round; fill:none;
           stroke-dasharray:.14 1.2; stroke-dashoffset:.14; opacity:0;
           animation: travel {PERIOD}s linear infinite }}
  .node {{ fill:{t['bg']}; stroke:{t['fg']}; stroke-width:2 }}
  .fire {{ fill:{t['accent']}; opacity:0; animation: fire {PERIOD}s ease-out infinite }}
  .eyebrow {{ font:600 14px {MONO}; letter-spacing:2.5px; fill:{t['accent']} }}
  .name {{ font:700 76px {SERIF}; fill:{t['fg']}; letter-spacing:-1px }}
  .tag {{ font:400 21px {SANS}; fill:{t['muted']} }}
  .chip {{ fill:none; stroke:{t['fg']}; stroke-opacity:.25 }}
  .chipt {{ font:500 12.5px {MONO}; fill:{t['fg']}; opacity:.8 }}
  .io {{ font:500 12.5px {MONO}; fill:{t['muted']} }}
  .caret {{ fill:{t['accent']}; animation: blink 1.1s steps(1) infinite }}
  @keyframes travel {{ 0% {{ stroke-dashoffset:.14; opacity:1 }} 22% {{ stroke-dashoffset:-1; opacity:1 }} 23%,100% {{ opacity:0 }} }}
  @keyframes fire {{ 0% {{ opacity:0 }} 6% {{ opacity:.95 }} 30%,100% {{ opacity:0 }} }}
  @keyframes blink {{ 50% {{ opacity:0 }} }}
  @media (prefers-reduced-motion: reduce) {{ .pulse, .fire, .caret {{ animation:none }} }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{t['bg']}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#dots)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t['fg']}" stroke-opacity=".12"/>
<text x="56" y="84" class="eyebrow">{esc(EYEBROW)}</text>
<text x="56" y="168" class="name">{esc(NAME)}<tspan fill="{t['accent']}">.</tspan></text>
{tagline}
{''.join(chips)}
<rect x="{cx + 2}" y="270" width="10" height="20" rx="2" class="caret"/>
{''.join(edges)}
{''.join(pulses)}
{''.join(circles)}
{''.join(labels)}
</svg>
"""


if __name__ == "__main__":
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    for mode in ("light", "dark"):
        (out / f"header-{mode}.svg").write_text(build(mode))
        print("wrote", out / f"header-{mode}.svg")
