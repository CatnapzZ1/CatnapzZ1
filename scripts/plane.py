"""Pixel paper plane used by sky.py."""
from PIL import Image, ImageDraw

# paper plane (telegram-style) rasterised onto a small pixel grid, then outlined
GW, GH = 22, 18                             # one cell of padding for the outline
UPPER = [(2, 8), (20, 2), (9, 11)]          # top wing
LOWER = [(9, 11), (20, 2), (12, 16)]        # bottom wing, past the fold
FLAP = [(9, 11), (12, 16), (9, 14)]         # small tucked tail
FILL = {1: "#ffffff", 2: "#d9e8f4", 3: "#a9c3dd"}
OUTLINE = "#6f95bd"

def grid():
    im = Image.new("L", (GW, GH), 0)
    d = ImageDraw.Draw(im)
    for poly, v in ((UPPER, 1), (LOWER, 2), (FLAP, 3)):
        d.polygon(poly, fill=v)
    g = [[im.getpixel((x, y)) for x in range(GW)] for y in range(GH)]
    out = [row[:] for row in g]
    for y in range(GH):
        for x in range(GW):
            if g[y][x] == 0 and any(
                0 <= x + dx < GW and 0 <= y + dy < GH and g[y + dy][x + dx]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = 9
    return out

def svg_group(s):
    g = grid()
    colors = {**FILL, 9: OUTLINE}
    parts = []
    for v, color in colors.items():
        d = "".join(f"M{x*s} {y*s}h{s}v{s}h-{s}z" for y in range(GH) for x in range(GW) if g[y][x] == v)
        if d:
            parts.append(f'<path fill="{color}" d="{d}"/>')
    return f'<g shape-rendering="crispEdges">{"".join(parts)}</g>'
