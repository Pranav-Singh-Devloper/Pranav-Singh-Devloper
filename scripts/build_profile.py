"""Daily profile refresh. Standard library only, so it can't break on a dependency.

1. Pulls my public GitHub activity and upstream PRs (GraphQL), plus LeetCode and Codeforces ratings.
2. Draws assets/generated/training-run-{light,dark}.svg, a W&B-style panel:
   weekly contributions as a "training curve" (raw + EMA-smoothed), metric
   tiles, and a language mix bar.
3. Draws assets/generated/activity-{light,dark}.svg, a radar of commits /
   issues / pull requests / code review, like GitHub's activity overview.
4. Rewrites the auto-updated parts of README.md between <!--NAME:START/END--> markers.

Env: GITHUB_TOKEN (or GH_TOKEN). Locally:  GH_TOKEN=$(gh auth token) python scripts/build_profile.py
"""

import datetime as dt
import json
import os
import re
import urllib.request
from collections import Counter
from pathlib import Path

from theme import MONO, SANS, SERIF, THEMES, esc

LOGIN = "Pranav-Singh-Devloper"
LEETCODE = "hawkeye_1"
CODEFORCES = "hawkeye_1"

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "assets" / "generated"

# Markup and config languages say little about the work.
IGNORED_LANGS = {
    "HTML", "CSS", "SCSS", "Jupyter Notebook", "Makefile", "Dockerfile", "Shell",
    "Batchfile", "PowerShell", "Procfile", "Mako", "Jinja", "MDX",
}
# Repos that shouldn't appear in "recently shipped".
SKIP_RECENT = {LOGIN, "harness-demo-taskboard", "harness-demo-recipes", "harness-demo-bookshop"}
# Owners whose repos don't count as upstream open source (course repos, my own demo org).
SKIP_UPSTREAM_OWNERS = {LOGIN, "CODERNSINGH", "MerakiWorks-1"}
STALE_OPEN_PR_DAYS = 180
# Fallback one-liners for repos without a GitHub description.
BLURBS = {
    "Engram": "Bitemporal memory for AI agents, served over MCP (Postgres + pgvector)",
    "The_Tokenizer": "BPE, byte-level BPE and WordPiece from scratch, GPT-2 parity, live visualizer",
    "nexus-project": "Research agent → cited market report → LinkedIn post, end to end",
    "ml-ab-testing": "Statistically rigorous A/B test of 3 models on 15 OpenML-CC18 datasets",
    "viberon-dmg": "AI dev environment: plans work and runs specialist agents in parallel",
    "traffic-oracle": "Graph attention (STGAT) traffic forecasting on METR-LA",
    "ColdCase_RAG": "Citation-first RAG over case files (FAISS + LangChain + Groq)",
}

NOT_MINE = " ".join(f"-user:{o}" for o in sorted(SKIP_UPSTREAM_OWNERS))

GQL = """
query($login: String!, $prq: String!, $isq: String!) {
  prs: search(query: $prq, type: ISSUE, first: 60) {
    nodes { ... on PullRequest {
      title url state merged createdAt
      repository { nameWithOwner url stargazerCount owner { login } }
    } }
  }
  issues: search(query: $isq, type: ISSUE, first: 1) { issueCount }
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions totalIssueContributions
      totalPullRequestContributions totalPullRequestReviewContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name description url stargazerCount pushedAt
        primaryLanguage { name }
      }
    }
  }
}
"""


# --------------------------------------------------------------------------- data

def http_json(url, payload=None, headers=None, timeout=20):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "profile-readme-bot", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def github():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("Set GITHUB_TOKEN or GH_TOKEN")
    res = http_json(
        "https://api.github.com/graphql",
        {"query": GQL, "variables": {
            "login": LOGIN,
            "prq": f"author:{LOGIN} is:pr {NOT_MINE} sort:created-desc",
            "isq": f"author:{LOGIN} is:issue {NOT_MINE}",
        }},
        {"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    if "errors" in res:
        raise SystemExit(f"GraphQL error: {res['errors']}")
    return res["data"]


def leetcode():
    try:
        q = {"query": "query($u:String!){userContestRanking(username:$u){rating} "
                      "matchedUser(username:$u){submitStatsGlobal{acSubmissionNum{difficulty count}}}}",
             "variables": {"u": LEETCODE}}
        d = http_json("https://leetcode.com/graphql", q,
                      {"Content-Type": "application/json", "Referer": "https://leetcode.com"})["data"]
        solved = next(x["count"] for x in d["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"] if x["difficulty"] == "All")
        rating = round(d["userContestRanking"]["rating"]) if d["userContestRanking"] else None
        return rating, solved
    except Exception as e:  # rate limits, Cloudflare, schema changes: keep the last known value
        print("leetcode: keeping previous values:", e)
        return None, None


def codeforces():
    try:
        u = http_json(f"https://codeforces.com/api/user.info?handles={CODEFORCES}")["result"][0]
        return u.get("rating"), u.get("maxRating")
    except Exception as e:
        print("codeforces: keeping previous values:", e)
        return None, None


def upstream(prs):
    """Merged PRs to other people's projects, plus open ones that aren't stale."""
    now = dt.datetime.now(dt.timezone.utc)
    keep = []
    for pr in prs:
        if not pr or pr["repository"]["owner"]["login"] in SKIP_UPSTREAM_OWNERS:
            continue
        age = (now - dt.datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))).days
        if pr["merged"] or (pr["state"] == "OPEN" and age <= STALE_OPEN_PR_DAYS):
            keep.append(pr)
    return keep


def kfmt(n):
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def upstream_table(prs, limit=10):
    merged = sum(pr["merged"] for pr in prs)
    repos = {pr["repository"]["nameWithOwner"] for pr in prs}
    lines = [
        f"**{merged} merged · {len(prs) - merged} in review · {len(repos)} repositories** "
        f"<sub>(auto-updated daily)</sub>",
        "",
        "| | project | pull request | status | opened |",
        "|:-:|:--|:--|:--|:--|",
    ]
    for pr in prs[:limit]:
        repo = pr["repository"]
        owner = repo["owner"]["login"]
        title = pr["title"].replace("|", "\\|")
        status = "🟣&nbsp;merged" if pr["merged"] else "🟢&nbsp;in&nbsp;review"
        when = dt.date.fromisoformat(pr["createdAt"][:10]).strftime("%b %Y")
        lines.append(
            f'| <img src="https://github.com/{owner}.png?size=40" width="20" height="20" alt="{owner}"> '
            f'| [{repo["nameWithOwner"]}]({repo["url"]}) <sub>★ {kfmt(repo["stargazerCount"])}</sub> '
            f'| [{title}]({pr["url"]}) | {status} | {when} |'
        )
    if not prs:
        lines = ["_First upstream pull requests in progress._"]
    return "\n".join(lines)


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    # Today isn't over yet, so a zero today doesn't break the streak.
    i = len(counts) - 1
    if counts and counts[i] == 0:
        i -= 1
    current = 0
    while i >= 0 and counts[i] > 0:
        current += 1
        i -= 1
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    return current, longest, sum(1 for c in counts if c > 0)


def language_mix(repos, top=5):
    """Share of my public repos by primary language. Counting repos instead of
    bytes stops vendored or generated code from drowning out real work."""
    total = Counter(
        r["primaryLanguage"]["name"] for r in repos
        if r["primaryLanguage"] and r["primaryLanguage"]["name"] not in IGNORED_LANGS
    )
    s = sum(total.values()) or 1
    items = [(name, n / s) for name, n in total.most_common(top)]
    rest = 1 - sum(p for _, p in items)
    if rest > 0.005:
        items.append(("Other", rest))
    return items


# --------------------------------------------------------------------------- svg

def smooth_path(pts, lo=None, hi=None):
    """Catmull-Rom spline through pts, as cubic Béziers. Control points are
    clamped to [lo, hi] in y so the curve never dips below zero."""
    def cl(y):
        if lo is not None:
            y = max(min(y, hi), lo)
        return y
    if len(pts) < 2:
        return ""
    d = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, cl(p1[1] + (p2[1] - p0[1]) / 6))
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, cl(p2[1] - (p3[1] - p1[1]) / 6))
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    return " ".join(d)


def fmt(n):
    if n is None:
        return "—"
    return f"{n / 1000:.1f}k" if n >= 10000 else f"{n:,}"


def render(mode, s):
    t = THEMES[mode]
    W, H = 1200, 470

    # chart panel
    cx, cy, cw, ch = 24, 76, 700, 270
    px0, px1 = cx + 44, cx + cw - 20
    py0, py1 = cy + 52, cy + ch - 34
    weekly = s["weekly"]
    step_y = max(1, -(-max(max(weekly), 4) // 4))  # ceil, so the peak fits under the top gridline
    ymax = step_y * 4
    n = len(weekly)

    def X(i):
        return px0 + (px1 - px0) * i / max(n - 1, 1)

    def Y(v):
        return py1 - (py1 - py0) * v / ymax

    raw = [(X(i), Y(v)) for i, v in enumerate(weekly)]
    ema, acc = [], weekly[0]
    for v in weekly:  # same smoothing knob W&B shows (0.6)
        acc = 0.6 * acc + 0.4 * v
        ema.append(acc)
    sm = [(X(i), Y(v)) for i, v in enumerate(ema)]
    sm_path = smooth_path(sm, py0, py1)
    area = f"{sm_path} L{px1:.1f},{py1:.1f} L{px0:.1f},{py1:.1f} Z"

    grid = []
    for k in range(5):
        v = step_y * k
        y = Y(v)
        grid.append(f'<line x1="{px0}" x2="{px1}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                    f'<text x="{px0 - 10}" y="{y + 4:.1f}" text-anchor="end" class="axis">{v}</text>')
    months, last = [], None
    for i, wk in enumerate(s["week_starts"]):
        m = wk.strftime("%b")
        if m != last and i < n - 2:
            months.append(f'<text x="{X(i):.1f}" y="{py1 + 20}" text-anchor="middle" class="axis">{m}</text>')
            last = m

    # tiles
    tiles = [
        ("upstream PRs merged", fmt(s["up_merged"])),
        ("upstream repos", fmt(s["up_repos"])),
        ("issues filed upstream", fmt(s["up_issues"])),
        ("contributions · 12 mo", fmt(s["total"])),
        ("current streak", f"{s['current']}d"),
        ("longest streak", f"{s['longest']}d"),
        ("public repos", fmt(s["repos"])),
        ("active days", fmt(s["active"])),
    ]
    tx0, ty0, tw, th, gx, gy = 744, 76, 210, 58, 12, 12
    tile_svg = []
    for k, (label, value) in enumerate(tiles):
        x = tx0 + (k % 2) * (tw + gx)
        y = ty0 + (k // 2) * (th + gy)
        tile_svg.append(
            f'<g class="tile" style="animation-delay:{0.15 + k * 0.07:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="12" class="panel"/>'
            f'<text x="{x + 16}" y="{y + 22}" class="label">{esc(label)}</text>'
            f'<text x="{x + 16}" y="{y + 47}" class="value">{esc(value)}</text></g>'
        )

    # language bar
    bx, by, bw = 24, 366, 1152
    mix = s["langs"]
    bar, legend, x, lx = [], [], bx + 20, bx + 20
    inner = bw - 40
    for k, (name, p) in enumerate(mix):
        color = t["series"][-1] if name == "Other" else t["series"][k % (len(t["series"]) - 1)]
        w = inner * p
        bar.append(f'<rect x="{x:.1f}" y="{by + 44}" width="{max(w - 2, 1):.1f}" height="12" rx="3" fill="{color}"/>')
        x += w
        label = f"{name} {p * 100:.0f}%"
        legend.append(f'<rect x="{lx}" y="{by + 72}" width="10" height="10" rx="2" fill="{color}"/>'
                      f'<text x="{lx + 16}" y="{by + 81}" class="legend">{esc(label)}</text>')
        lx += 34 + len(label) * 7.6

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub activity for {LOGIN}">
<title>Training run: {s['total']} contributions in the last 12 months, {s['current']}-day current streak</title>
<defs>
  <linearGradient id="fill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{t['accent']}" stop-opacity=".28"/>
    <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
  .panel {{ fill:{t['panel']}; stroke:{t['line']} }}
  .grid {{ stroke:{t['line']}; stroke-dasharray:3 4 }}
  .axis {{ font:500 11px {MONO}; fill:{t['muted']} }}
  .title {{ font:600 13px {MONO}; fill:{t['fg']}; letter-spacing:.4px }}
  .sub {{ font:500 11.5px {MONO}; fill:{t['muted']} }}
  .label {{ font:500 11px {MONO}; fill:{t['muted']}; letter-spacing:.3px }}
  .value {{ font:700 22px {SERIF}; fill:{t['fg']} }}
  .legend {{ font:500 12px {SANS}; fill:{t['fg']} }}
  .head {{ font:600 13px {MONO}; fill:{t['fg']} }}
  .headm {{ font:500 13px {MONO}; fill:{t['muted']} }}
  .raw {{ fill:none; stroke:{t['accent']}; stroke-opacity:.35; stroke-width:1.2; stroke-linejoin:round }}
  .ema {{ fill:none; stroke:{t['accent']}; stroke-width:2.6; stroke-linecap:round;
          stroke-dasharray:1; stroke-dashoffset:0; animation: draw 2.4s cubic-bezier(.3,.7,.2,1) both }}
  .area {{ fill:url(#fill); animation: fade 2.4s ease-out both }}
  .tile {{ animation: rise .6s ease-out both }}
  .live {{ fill:{t['accent']}; animation: pulse 1.6s ease-in-out infinite }}
  @keyframes draw {{ from {{ stroke-dashoffset:1 }} to {{ stroke-dashoffset:0 }} }}
  @keyframes fade {{ from {{ opacity:0 }} to {{ opacity:1 }} }}
  @keyframes rise {{ from {{ opacity:0; transform:translateY(6px) }} to {{ opacity:1; transform:none }} }}
  @keyframes pulse {{ 50% {{ opacity:.25 }} }}
  @media (prefers-reduced-motion: reduce) {{ .ema, .area, .tile, .live {{ animation:none }} }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{t['bg']}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t['fg']}" stroke-opacity=".12"/>

<circle cx="40" cy="40" r="5" class="live"/>
<text x="54" y="44" class="head">run: pranav-singh/{s['year']}<tspan class="headm" dx="14">status: training · step {s['total']:,} · refreshed {s['updated']}</tspan></text>

<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" class="panel"/>
<text x="{cx + 20}" y="{cy + 28}" class="title">contributions / week</text>
<text x="{cx + cw - 20}" y="{cy + 28}" text-anchor="end" class="sub">this week: {weekly[-1]} · raw ── · ema(0.6) ━━</text>
{''.join(grid)}
{''.join(months)}
<path d="{area}" class="area"/>
<polyline points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in raw)}" class="raw"/>
<path d="{sm_path}" pathLength="1" class="ema"/>
<circle cx="{sm[-1][0]:.1f}" cy="{sm[-1][1]:.1f}" r="4.5" fill="{t['accent']}" class="live"/>

{''.join(tile_svg)}

<rect x="{bx}" y="{by}" width="{bw}" height="{98}" rx="14" class="panel"/>
<text x="{bx + 20}" y="{by + 28}" class="title">training data mix</text>
<text x="{bx + bw - 20}" y="{by + 28}" text-anchor="end" class="sub">primary language of each public repo · markup excluded</text>
{''.join(bar)}
{''.join(legend)}
</svg>
"""


ACTIVITY_AXES = [  # clockwise from the top, the same layout GitHub uses
    ("Code review", "totalPullRequestReviewContributions"),
    ("Issues", "totalIssueContributions"),
    ("Pull requests", "totalPullRequestContributions"),
    ("Commits", "totalCommitContributions"),
]


def activity_mix(cc):
    counts = [(name, cc[key]) for name, key in ACTIVITY_AXES]
    total = sum(n for _, n in counts) or 1
    return [(name, n, n / total) for name, n in counts]


def render_activity(mode, s):
    t = THEMES[mode]
    W, H = 1200, 400
    mix = s["activity"]
    total = sum(n for _, n, _ in mix)
    pmax = max(p for _, _, p in mix) or 1

    # radar panel
    rx, ry, rw, rh = 24, 72, 560, 304
    cx, cy = rx + rw / 2, ry + rh / 2
    arm = {"Code review": (0, -1, 100), "Issues": (1, 0, 150),
           "Pull requests": (0, 1, 100), "Commits": (-1, 0, 150)}
    pts, arms, labels = [], [], []
    for k, (name, n, p) in enumerate(mix):
        dx, dy, L = arm[name]
        r = 6 + (L - 6) * p / pmax  # scaled to the biggest share, as GitHub does
        pts.append((dx * r, dy * r))
        arms.append(f'<line x1="0" y1="0" x2="{dx * L}" y2="{dy * L}" class="arm"/>')
        pct = f"{round(p * 100)}%"
        if dy:  # top / bottom: percent, then name, stacked away from the arm
            y = cy + dy * (L + 28) if dy < 0 else cy + L + 20
            labels.append(f'<text x="{cx}" y="{y:.0f}" text-anchor="middle" class="pct">{pct}</text>'
                          f'<text x="{cx}" y="{y + 18:.0f}" text-anchor="middle" class="axisname">{esc(name)}</text>')
        else:
            x = cx + dx * (L + 18)
            anchor = "end" if dx < 0 else "start"
            labels.append(f'<text x="{x:.0f}" y="{cy - 4:.0f}" text-anchor="{anchor}" class="pct">{pct}</text>'
                          f'<text x="{x:.0f}" y="{cy + 14:.0f}" text-anchor="{anchor}" class="axisname">{esc(name)}</text>')
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" class="dot"/>' for x, y in pts)

    # breakdown panel
    bx, by, bw, bh = 600, 72, 576, 304
    track0, track1 = bx + 150, bx + bw - 86
    rows = []
    for k, (name, n, p) in enumerate(sorted(mix, key=lambda m: -m[1])):
        y = by + 84 + k * 52
        w = max((track1 - track0) * p, 3) if n else 0
        rows.append(
            f'<g class="row" style="animation-delay:{0.2 + k * 0.08:.2f}s">'
            f'<text x="{bx + 20}" y="{y}" class="rowname">{esc(name)}</text>'
            f'<text x="{bx + 20}" y="{y + 18}" class="label">{n:,}</text>'
            f'<rect x="{track0}" y="{y - 4}" width="{track1 - track0}" height="10" rx="5" class="track"/>'
            f'<rect x="{track0}" y="{y - 4}" width="{w:.1f}" height="10" rx="5" fill="{t["accent"]}"/>'
            f'<text x="{bx + bw - 20}" y="{y + 7}" text-anchor="end" class="value">{round(p * 100)}%</text></g>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Activity overview for {LOGIN}">
<title>Activity overview, last 12 months: {', '.join(f'{name} {round(p * 100)}%' for name, _, p in mix)}</title>
<style>
  .panel {{ fill:{t['panel']}; stroke:{t['line']} }}
  .head {{ font:600 13px {MONO}; fill:{t['fg']} }}
  .headm {{ font:500 13px {MONO}; fill:{t['muted']} }}
  .title {{ font:600 13px {MONO}; fill:{t['fg']}; letter-spacing:.4px }}
  .sub {{ font:500 11.5px {MONO}; fill:{t['muted']} }}
  .label {{ font:500 11px {MONO}; fill:{t['muted']}; letter-spacing:.3px }}
  .value {{ font:700 20px {SERIF}; fill:{t['fg']} }}
  .rowname {{ font:600 14px {SANS}; fill:{t['fg']} }}
  .pct {{ font:700 17px {SERIF}; fill:{t['fg']} }}
  .axisname {{ font:500 13px {SANS}; fill:{t['muted']} }}
  .arm {{ stroke:{t['accent']}; stroke-width:2.2; stroke-linecap:round; stroke-opacity:.85 }}
  .shape {{ fill:{t['accent']}; fill-opacity:.32; stroke:{t['accent']}; stroke-width:2.2; stroke-linejoin:round }}
  .dot {{ fill:{t['panel']}; stroke:{t['accent']}; stroke-width:2.6 }}
  .track {{ fill:{t['line']}; opacity:.6 }}
  .grow {{ animation: grow 1.2s cubic-bezier(.3,.7,.2,1) both }}
  .row {{ animation: rise .6s ease-out both }}
  .live {{ fill:{t['accent']}; animation: pulse 1.6s ease-in-out infinite }}
  @keyframes grow {{ from {{ transform:scale(0); opacity:0 }} to {{ transform:scale(1); opacity:1 }} }}
  @keyframes rise {{ from {{ opacity:0; transform:translateY(6px) }} to {{ opacity:1; transform:none }} }}
  @keyframes pulse {{ 50% {{ opacity:.25 }} }}
  @media (prefers-reduced-motion: reduce) {{ .grow, .row, .live {{ animation:none }} }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{t['bg']}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t['fg']}" stroke-opacity=".12"/>

<circle cx="40" cy="40" r="5" class="live"/>
<text x="54" y="44" class="head">activity overview<tspan class="headm" dx="14">last 12 months · {total:,} contributions · refreshed {s['updated']}</tspan></text>

<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="14" class="panel"/>
<g transform="translate({cx},{cy})">
  {''.join(arms)}
  <g class="grow"><polygon points="{poly}" class="shape"/>{dots}</g>
</g>
{''.join(labels)}

<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="14" class="panel"/>
<text x="{bx + 20}" y="{by + 28}" class="title">contribution mix</text>
<text x="{bx + bw - 20}" y="{by + 28}" text-anchor="end" class="sub">share of commits, issues, PRs and reviews</text>
{''.join(rows)}
</svg>
"""


# --------------------------------------------------------------------------- readme

def replace_block(text, name, body):
    pat = re.compile(rf"(<!--{name}:START-->)(.*?)(<!--{name}:END-->)", re.S)
    return pat.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text) if pat.search(text) else text


def previous(text, key):
    m = re.search(rf"^\s*{key}:\s*([0-9]+)", text, re.M)
    return int(m.group(1)) if m else None


def ago(iso):
    days = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    return "today" if days == 0 else "yesterday" if days == 1 else f"{days} days ago"


def main():
    data = github()
    user = data["user"]
    up = upstream(data["prs"]["nodes"])
    readme = README.read_text()

    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    current, longest, active = streaks(days)
    repos = user["repositories"]["nodes"]

    lc_rating, lc_solved = leetcode()
    cf_rating, cf_max = codeforces()
    lc_rating = lc_rating or previous(readme, "leetcode_contest_rating")
    lc_solved = lc_solved or previous(readme, "leetcode_solved")
    cf_max = cf_max or previous(readme, "codeforces_max_rating")

    today = dt.datetime.now(dt.timezone.utc).date()
    stats = {
        "weekly": [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks],
        "week_starts": [dt.date.fromisoformat(w["contributionDays"][0]["date"]) for w in weeks],
        "total": cal["totalContributions"],
        "current": current, "longest": longest, "active": active,
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "up_merged": sum(pr["merged"] for pr in up),
        "up_repos": len({pr["repository"]["nameWithOwner"] for pr in up}),
        "up_issues": data["issues"]["issueCount"],
        "lc_rating": lc_rating, "cf_max": cf_max,
        "langs": language_mix(repos),
        "activity": activity_mix(user["contributionsCollection"]),
        "updated": today.isoformat(), "year": today.year,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    for mode in ("light", "dark"):
        (OUT / f"training-run-{mode}.svg").write_text(render(mode, stats))
        (OUT / f"activity-{mode}.svg").write_text(render_activity(mode, stats))

    # model card numbers
    def card(block):
        for key, val in [
            ("public_repos", stats["repos"]),
            ("contributions_last_12mo", stats["total"]),
            ("leetcode_contest_rating", lc_rating),
            ("leetcode_solved", lc_solved),
            ("codeforces_max_rating", cf_max),
        ]:
            if val is not None:
                block = re.sub(rf"^(\s*{key}:\s*)\S+", rf"\g<1>{val}", block, flags=re.M)
        return re.sub(r"(last_trained:\s*)\S+", rf"\g<1>{today.isoformat()}", block)

    readme = re.sub(r"(<!--CARD:START-->)(.*?)(<!--CARD:END-->)",
                    lambda m: m.group(1) + card(m.group(2)) + m.group(3), readme, flags=re.S)

    readme = replace_block(readme, "UPSTREAM", upstream_table(up))

    # recently shipped
    rows = ["| repo | what | lang | pushed |", "|:--|:--|:--|:--|"]
    for r in [r for r in repos if r["name"] not in SKIP_RECENT][:5]:
        what = r["description"] or BLURBS.get(r["name"], "")
        what = re.sub(r"\s+", " ", what).replace("|", "\\|")
        if len(what) > 90:
            what = what[:87].rstrip() + "…"
        lang = (r["primaryLanguage"] or {}).get("name", "")
        rows.append(f"| [**{r['name']}**]({r['url']}) | {what} | `{lang}` | {ago(r['pushedAt'])} |")
    readme = replace_block(readme, "RECENT", "\n".join(rows))

    README.write_text(readme)
    print(json.dumps({k: v for k, v in stats.items() if k not in ("weekly", "week_starts", "activity")}, default=str, indent=1))


if __name__ == "__main__":
    main()
