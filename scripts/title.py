"""Build assets/title.svg and title-dark.svg: the pixel-font name with a sleeping cat.

Usage: python3 title.py <ark-pixel-12px-monospaced-latin.otf> <text> <out-prefix>
"""
import sys
from PIL import Image, ImageDraw, ImageFont

font_path, text, out_prefix = sys.argv[1], sys.argv[2], sys.argv[3]
font = ImageFont.truetype(font_path, 12)
S = 4          # screen px per font pixel
W_CELL, H_CELL = 6, 12   # monospaced latin cell

im = Image.new("1", (W_CELL * len(text), H_CELL), 0)
ImageDraw.Draw(im).text((0, 0), text, font=font, fill=1)
# trim empty rows so the title sits tight
rows = [y for y in range(H_CELL) if any(im.getpixel((x, y)) for x in range(im.width))]
top, bottom = rows[0], rows[-1] + 1

def runs(dx, dy):
    d = []
    for y in range(top, bottom):
        x = 0
        while x < im.width:
            if im.getpixel((x, y)):
                x0 = x
                while x < im.width and im.getpixel((x, y)):
                    x += 1
                d.append(f"M{(x0+dx)*S} {(y-top+dy)*S}h{(x-x0)*S}v{S}h-{(x-x0)*S}z")
            else:
                x += 1
    return "".join(d)

w, h = (im.width + 1) * S, (bottom - top + 1) * S

# sleeping pixel cat to the right of the name, same pixel grain as the glyphs
CAT = """
.................ZZZ
...................Z
..................Z.
.................ZZZ
............zz......
.............z......
.............zz.....
..O.....O...........
..OO...OO...........
..OBOOOBO...........
.OBBBBBBBOOOOOOO....
.OBEBBBEBBBBBBBBO...
.OBBBEBBBBBBBBBBBO..
.OBBBBBBBBBBBBBBBO..
..OTTTTTTTTTTOBBBO..
...OOOOOOOOOOOOOO...
""".strip("\n").split("\n")
CAT_W, CAT_H = len(CAT[0]) * S, len(CAT) * S
GAP = 2 * S
# baseline = lowest pixel row of the first glyph ("C" has no descender)
base = max(y for y in range(top, bottom) for x in range(W_CELL) if im.getpixel((x, y))) - top + 1
W = w + GAP + CAT_W
TY = max(0, CAT_H - base * S)    # shift the title down so the cat sits on its baseline
H = max(TY + h, CAT_H)

def cat(col):
    layers = {}
    for cy, row in enumerate(CAT):
        for cx, ch in enumerate(row):
            if ch in col:
                layers.setdefault(ch, []).append(f"M{cx*S} {cy*S}h{S}v{S}h-{S}z")
    body = "".join(f'<path fill="{col[ch]}" d="{"".join(d)}"/>' for ch, d in layers.items() if ch not in "zZ")
    # snore loop: small z appears, then big Z, then both fade out
    snore = "".join(
        f'<path fill="{col[ch]}" d="{"".join(layers[ch])}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{at};0.8" calcMode="discrete" dur="3s" repeatCount="indefinite"/></path>'
        for ch, at in (("z", 0.25), ("Z", 0.5)))
    return f'<g transform="translate({w + GAP} {TY + base * S - CAT_H})">{body}{snore}</g>'

def build(fg, shadow, cat_col):
    return (f'<!-- Glyphs: Ark Pixel Font 12px (https://github.com/TakWolf/ark-pixel-font), SIL OFL 1.1 -->\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{text}">\n'
            f'<g transform="translate(0 {TY})"><path fill="{shadow}" d="{runs(1, 1)}"/>\n<path fill="{fg}" d="{runs(0, 0)}"/></g>\n'
            f'{cat(cat_col)}\n</svg>\n')

LIGHT_CAT = {"O": "#57606a", "B": "#f3e9ee", "E": "#57606a", "T": "#c7acbb", "z": "#88d9ec", "Z": "#2f64a6"}
DARK_CAT = {"O": "#c9d1d9", "B": "#3a3340", "E": "#c9d1d9", "T": "#c7acbb", "z": "#2f64a6", "Z": "#88d9ec"}
open(out_prefix + ".svg", "w").write(build("#2f64a6", "#c7acbb", LIGHT_CAT))
open(out_prefix + "-dark.svg", "w").write(build("#88d9ec", "#6b5a66", DARK_CAT))
print(W, H)
