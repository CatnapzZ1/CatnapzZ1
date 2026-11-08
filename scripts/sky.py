"""Build assets/sky.svg: pixel clouds, a paper plane and petals beside the cover.

Usage: python3 sky.py <out.svg>
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plane import svg_group as plane_pixels

out_path = sys.argv[1]
W, H = 380, 352                         # tall enough to end level with the cover beside it
K = H / 280                             # layout below was drawn for 280px; stretch it vertically
S = 4                                   # px per art pixel, same grain as the title
rnd = random.Random(5)

CLOUD = [
    "......HHHH........",
    "....HHWWWWHH.HHH..",
    "..HHWWWWWWWWHWWWH.",
    ".HWWWWWWWWWWWWWWWH",
    "HWWWWWWWWWWWWWWWWW",
    ".SSSSSSSSSSSSSSSS.",
]
SMALL_CLOUD = [
    "...HHH....",
    ".HHWWWHHH.",
    "HWWWWWWWWH",
    ".SSSSSSSS.",
]
MEDIUM_CLOUD = [
    "....HHH.......",
    "..HHWWWHHHH...",
    ".HWWWWWWWWWHH.",
    "HWWWWWWWWWWWWH",
    ".SSSSSSSSSSSS.",
]
COL = {"H": "#eef8fc", "W": "#d3ecf7", "S": "#a9d6ea"}

def pix(art, s):
    out = []
    for ch, color in COL.items():
        d = "".join(f"M{x*s} {y*s}h{s}v{s}h-{s}z"
                    for y, row in enumerate(art) for x, c in enumerate(row) if c == ch)
        if d:
            out.append(f'<path fill="{color}" d="{d}"/>')
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'

nodes = []
# clouds drift slowly back and forth, laid out on a zigzag (big / small / medium / small)
# and kept clear of the plane's flight line; neighbours drift in opposite directions
# (integer pixel scale only, so the grid stays crisp; size varies by art instead)
for art, x, y, dx, dur in [(CLOUD, 24, 30, 18, 22), (SMALL_CLOUD, 292, 16, -14, 18),
                           (MEDIUM_CLOUD, 196, 132, 16, 24), (SMALL_CLOUD, 58, 204, -12, 20)]:
    y = round(y * K / S) * S                # stay on the pixel grid
    nodes.append(
        f'<g transform="translate({x} {y})"><animateTransform attributeName="transform" type="translate" '
        f'values="{x} {y};{x + dx} {y};{x} {y}" dur="{dur}s" repeatCount="indefinite"/>'
        f'{pix(art, S)}</g>')

# a paper plane gliding across on a gentle wave, then a pause off-canvas
pts = []
for k in range(41):
    t = k / 40
    pts.append(f"{-60 + t * (W + 120):.1f} {(150 - 70 * t + 10 * math.sin(t * 2 * math.pi)) * K:.1f}")
nodes.append(
    f'<g><animateMotion dur="14s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.7;1" calcMode="linear" '
    f'path="M{"L".join(pts)}"/><g transform="translate(-22 -18)">{plane_pixels(2)}</g></g>')

# a few petals, same shape as on the cover
PETAL = ("M0 6C-2.4 5.2-3.5 0.6-3.2-2.6C-2.9-4.9-1.7-5.8-0.6-5.3L0.1-4.7L0.7-5.4"
         "C1.9-5.9 3.4-5 3.6-2.6C3.9 0.6 2.6 5.1 0 6Z")
for i in range(7):
    x = (i + 0.5) * W / 7 + rnd.uniform(-15, 15)
    dur, begin = rnd.uniform(8, 12), -rnd.uniform(0, 12)
    amp, sc = rnd.uniform(10, 24), rnd.uniform(1.1, 1.6)
    path = "M" + "L".join(f"{x + amp * math.sin(t / 30 * 2 * math.pi):.1f} {-15 + t / 30 * (H + 30):.1f}" for t in range(31))
    nodes.append(
        f'<g opacity="0.9"><animateMotion dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite" path="{path}"/>'
        f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="{rnd.choice([-1, 1]) * 240}" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
        f'<use href="#petal" transform="scale({sc:.2f})"/></g></g>')

for x, y, r, d in [(150, 44, 6, -0.3), (344, 92, 7, -1.5), (30, 150, 6, -2.2), (300, 236, 5, -0.9)]:
    y = round(y * K)
    nodes.append(
        f'<path transform="translate({x} {y})" d="M0 {-r}Q0 0 {r} 0Q0 0 0 {r}Q0 0 {-r} 0Q0 0 0 {-r}Z" fill="#88d9ec">'
        f'<animate attributeName="opacity" values="1;0.35;1" dur="3.2s" begin="{d}s" repeatCount="indefinite"/></path>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" overflow="hidden" role="img" aria-label="Pixel clouds and a paper plane drifting through falling sakura petals">
<defs>
<linearGradient id="petal-fill" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#efb9cb"/><stop offset="1" stop-color="#fdf1f5"/></linearGradient>
<path id="petal" d="{PETAL}" fill="url(#petal-fill)" stroke="#e3a6bb" stroke-width="0.3"/>
</defs>
{chr(10).join(nodes)}
</svg>
'''
open(out_path, "w").write(svg)
print(W, H)
