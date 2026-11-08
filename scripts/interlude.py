"""Build assets/interlude.svg: wavy staff with pixel notes, the divider and an eraser.

Usage: python3 interlude.py <out.svg>
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eraser import eraser, DEFS as ERASER_DEFS, crumbs

S = 3                                   # px per art pixel
EIGHTH = ["...XX..", "...XXX.", "...X.XX", "...X..X", "...X...", "...X...",
          ".XXX...", "XXXX...", "XXXX...", ".XX...."]
BEAMED = ["...XXXXXXX", "...XXXXXXX", "...X.....X", "...X.....X", "...X.....X", "...X.....X",
          ".XXX...XXX", "XXXX..XXXX", "XXXX..XXXX", ".XX....XX."]
QUARTER = ["...X", "...X", "...X", "...X", "...X", ".XXX", "XXXX", "XXXX", ".XX."]

BLUE, PINK, CYAN = "#4b8bd4", "#c7acbb", "#88d9ec"
W, H = 800, 80
CY = 50                                   # centre line of the staff
GAP = 6                                   # distance between staff lines
AMP, WAVE = 7, 300                        # the staff undulates gently across the width

def line_y(i, x):
    # y of staff line i (0 = top) at horizontal position x
    return CY + (i - 2) * GAP + AMP * math.sin(2 * math.pi * x / WAVE)

def note(art, color, x, y, delay):
    d = "".join(f"M{cx*S} {cy*S}h{S}v{S}h-{S}z"
                for cy, row in enumerate(art) for cx, c in enumerate(row) if c == "X")
    # hop one art pixel at a time so the motion keeps the pixel feel
    return (f'<g transform="translate({x} {y})"><animateTransform attributeName="transform" type="translate" '
            f'values="{x} {y};{x} {y - S};{x} {y - 2 * S};{x} {y - S}" dur="2.4s" begin="{delay}s" '
            f'calcMode="discrete" repeatCount="indefinite"/><path fill="{color}" d="{d}"/></g>')

def on_staff(art, color, x, line, delay):
    # place the note so its head (bottom rows of the art) sits on the given staff line
    head_x, head_y = 1.5 * S, (len(art) - 2) * S
    y = round((line_y(line, x + head_x) - head_y) / S) * S
    return note(art, color, x, y, delay)

# the pixel divider, same squares as assets/divider.svg, sitting on the middle staff line
DIV = ["#bfe6f2", "#88d9ec", "#4b8bd4", "#2f64a6", "#c7acbb", "#2f64a6", "#4b8bd4", "#88d9ec", "#bfe6f2"]
DS, DG = 6, 6
DW = len(DIV) * (DS + DG) - DG
DX = (W - DW) // 2
DY = round(line_y(2, W / 2) - DS / 2)
divider = "".join(f'<rect x="{DX + i * (DS + DG)}" y="{DY}" width="{DS}" height="{DS}" fill="{c}"/>' for i, c in enumerate(DIV))

# two staff halves flowing in from the edges and fading out before the divider
def staff(x0, x1, gid, fade_in_left):
    pts = lambda i: "M" + "L".join(f"{x:.0f} {line_y(i, x):.1f}" for x in range(x0, x1 + 1, 4))
    stops = ('<stop offset="0" stop-opacity="0"/><stop offset="0.12" stop-opacity="1"/>'
             '<stop offset="0.8" stop-opacity="1"/><stop offset="1" stop-opacity="0"/>')
    grad = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0 if fade_in_left else x1}" y1="0" '
            f'x2="{x1 if fade_in_left else x0}" y2="0">{stops.replace("/>", f' stop-color="{CYAN}"/>')}</linearGradient>')
    lines = "".join(f'<path d="{pts(i)}" fill="none" stroke="url(#{gid})" stroke-width="1.5" opacity="0.75"/>' for i in range(5))
    return grad, lines

g1, s1 = staff(0, DX - 24, "staff-l", True)
# the right half ends under an eraser that has just rubbed the staff out
EX = W - 46
EY = round(line_y(2, EX - 24)) + 1      # rest the rubber end on the staff it is erasing
TIP = EX - 30                           # where the rubber end touches the staff
g2, s2 = staff(DX + DW + 24, TIP - 26, "staff-r", False)
# just before the tip the lines are only half rubbed out: broken, patchy dashes
half = "".join(
    f'<path d="M{"L".join(f"{x} {line_y(i, x):.1f}" for x in range(TIP - 46, TIP + 1, 2))}" fill="none" stroke="{CYAN}" '
    f'stroke-width="1.5" stroke-dasharray="{4 + i % 2} {3 + i} 2 {5 - i % 3}" opacity="{0.45 - i * 0.04:.2f}"/>'
    for i in range(5))
smudge = f'<ellipse cx="{TIP - 14}" cy="{CY + 2}" rx="34" ry="20" fill="url(#smudge)"/>'
rubbed = crumbs([      # shavings gathered around the tip, a few strays along the half-erased lines
    (TIP - 6, line_y(4, TIP - 6) + 4, 4.5, 24), (TIP - 15, line_y(3, TIP - 15) + 2, 3.5, -30),
    (TIP + 2, line_y(4, TIP + 2) + 8, 3.5, 64), (TIP - 26, line_y(4, TIP - 26) + 5, 3, -12),
    (TIP - 9, line_y(2, TIP - 9) - 1, 2.5, 40), (TIP - 38, line_y(3, TIP - 38) + 1, 2.5, 18),
])

NOTES = [
    (BEAMED, BLUE, 44, 3, 0), (EIGHTH, PINK, 124, 1, -0.8), (QUARTER, CYAN, 196, 2, -1.6), (EIGHTH, BLUE, 268, 0, -0.4),
    (QUARTER, PINK, 516, 1, -1.2), (BEAMED, BLUE, 576, 3, -2.0), (EIGHTH, PINK, 646, 0, -0.6),
]
TOP = min(round((line_y(line, x + 1.5 * S) - (len(art) - 2) * S) / S) * S for art, _, x, line, _ in NOTES) - 2 * S - 2
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H - TOP}" viewBox="0 {TOP} {W} {H - TOP}" role="presentation">\n'
       f'<defs>{g1}{g2}{ERASER_DEFS}</defs>\n{smudge}\n{s1}\n{s2}\n{half}\n<g shape-rendering="crispEdges">{divider}\n'
       + "\n".join(on_staff(*n) for n in NOTES) + f"</g>\n{rubbed}\n{eraser(EX, EY)}\n</svg>\n")
open(sys.argv[1], "w").write(svg)
