"""Build assets/cover.svg: the illustration with sakura branches and falling petals.

Usage: python3 cover.py <illustration.jpg> <out.svg>
"""
import base64, io, math, random, sys
from PIL import Image

img_path, out_path = sys.argv[1], sys.argv[2]
IMG_W = 240                      # display width of the cover inside the canvas
src = Image.open(img_path).convert("RGB")
IMG_H = round(IMG_W * src.height / src.width)
W, H = 420, IMG_H                # floated to the right of the README text
IMG_X = 120                      # wider left margin faces the text; branches enter from the right edge
COUNT = 16
rnd = random.Random(11)

# sakura petal centred on the origin: narrow base at the bottom, notched tip on top
PETAL = ("M0 6C-2.4 5.2-3.5 0.6-3.2-2.6C-2.9-4.9-1.7-5.8-0.6-5.3L0.1-4.7L0.7-5.4"
         "C1.9-5.9 3.4-5 3.6-2.6C3.9 0.6 2.6 5.1 0 6Z")

def fall_path(x, amp, waves):
    # gentle sine drift from above the canvas to below it
    pts, steps = [], 48
    for k in range(steps + 1):
        t = k / steps
        y = -20 + t * (H + 40)
        pts.append(f"{x + amp * math.sin(t * waves * 2 * math.pi):.1f} {y:.1f}")
    return "M" + "L".join(pts)

# ---- static decoration in the side margins -------------------------------
L, R = IMG_X, IMG_X + IMG_W          # cover edges

def blossom(x, y, r, rot=0, op=1.0):
    # five petals radiating from the centre; r is the flower radius in px
    k = r / 11
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({k:.2f})" opacity="{op}">'
            + "".join(f'<use href="#petal" transform="rotate({a * 72}) translate(0 -6)"/>' for a in range(5))
            + '<circle r="1.8" fill="#f6dbe4"/>'
            + "".join(f'<circle cx="{1.6 * math.cos(a):.2f}" cy="{1.6 * math.sin(a):.2f}" r="0.45" fill="#d97f9f"/>'
                      for a in [i * 2 * math.pi / 6 for i in range(6)])
            + '</g>')

def bud(x, y, rot):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale(0.75)">'
            '<use href="#petal"/></g>')

def sparkle(x, y, r, delay):
    d = f"M0 {-r}Q0 0 {r} 0Q0 0 0 {r}Q0 0 {-r} 0Q0 0 0 {-r}Z"
    return (f'<path transform="translate({x} {y})" d="{d}" fill="#88d9ec">'
            f'<animate attributeName="opacity" values="1;0.35;1" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/></path>')

BRANCH = 'fill="none" stroke="#a8919e" stroke-linecap="round"'
decor = [
    # top branch entering from the page edge over the sky
    f'<path {BRANCH} stroke-width="3.2" d="M{W + 6} 34C{W - 50} 30 {W - 100} 52 {R - 60} 86"/>',
    f'<path {BRANCH} stroke-width="1.6" d="M{W - 44} 33C{W - 56} 16 {W - 70} 16 {W - 86} 16"/>',
    f'<path {BRANCH} stroke-width="1.4" d="M{W - 96} 56C{W - 100} 70 {W - 104} 84 {W - 104} 98"/>',
    blossom(R - 60, 84, 13, -8), blossom(W - 86, 16, 10, 10), blossom(W - 104, 100, 9, 30),
    blossom(W - 22, 30, 11, 20), bud(R - 80, 96, 140), bud(W - 66, 20, -40),
    # lower branch from the same edge, as if one tree stands just off the page
    f'<path {BRANCH} stroke-width="3.2" d="M{W + 6} {H - 96}C{W - 40} {H - 92} {W - 80} {H - 108} {R - 30} {H - 136}"/>',
    f'<path {BRANCH} stroke-width="1.6" d="M{W - 50} {H - 96}C{W - 60} {H - 74} {W - 74} {H - 62} {W - 90} {H - 56}"/>',
    blossom(R - 30, H - 138, 13, 12), blossom(W - 30, H - 94, 11, 0), blossom(W - 90, H - 56, 10, -20),
    bud(R - 48, H - 148, -60),
    # loose blossoms and twinkles in the margin between the text and the cover
    blossom(34, H * 0.16, 7, 15), blossom(90, H * 0.32, 5, 40), blossom(40, H * 0.5, 6, 0), blossom(96, H * 0.64, 5, 25),
    sparkle(70, H * 0.08, 6, -0.4), sparkle(20, H * 0.36, 7, -1.6), sparkle(78, H * 0.48, 5, -2.4), sparkle(30, H * 0.7, 6, -1.1),
    sparkle(W - 24, H * 0.42, 6, -2.0), blossom(W - 30, H * 0.56, 6, 50),
]

decor += [blossom(L - 60, H - 40, 8, 20), sparkle(L - 92, H - 70, 5, -1.3)]  # bottom-left corner

petals = []
for i in range(COUNT):
    # spread evenly across the width with some jitter so neither side clumps
    x = (i + 0.5) * W / COUNT + rnd.uniform(-0.4, 0.4) * W / COUNT
    dur = rnd.uniform(7, 11)
    begin = -rnd.uniform(0, dur)                    # already mid-fall on load
    scale = rnd.uniform(1.1, 1.8)
    spin = rnd.choice([-1, 1]) * rnd.randint(120, 300)
    tumble = rnd.uniform(1.6, 3.2)
    petals.append(f'''<g opacity="{rnd.uniform(0.75, 0.95):.2f}">
<animateMotion dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite" path="{fall_path(x, rnd.uniform(12, 30), rnd.uniform(0.8, 1.6))}"/>
<g><animateTransform attributeName="transform" type="rotate" from="0" to="{spin}" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>
<g><animateTransform attributeName="transform" type="scale" values="{scale:.2f} {scale:.2f};{scale*0.35:.2f} {scale:.2f};{scale:.2f} {scale:.2f}" dur="{tumble:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>
<use href="#petal"/></g></g></g>''')

# embed at 2x the display size: sharp on hi-dpi screens without bloating the svg
buf = io.BytesIO()
src.resize((IMG_W * 2, IMG_H * 2), Image.LANCZOS).save(buf, "JPEG", quality=85, optimize=True, progressive=True)
data = base64.b64encode(buf.getvalue()).decode()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" overflow="hidden" role="img" aria-label="Illustration of a girl leaning on a railing under a blue sky, framed by sakura branches with petals drifting down">
<defs>
<linearGradient id="petal-fill" x1="0" y1="1" x2="0" y2="0">
<stop offset="0" stop-color="#efb9cb"/><stop offset="1" stop-color="#fdf1f5"/>
</linearGradient>
<path id="petal" d="{PETAL}" fill="url(#petal-fill)" stroke="#e3a6bb" stroke-width="0.3"/>
</defs>
<image x="{IMG_X}" y="0" width="{IMG_W}" height="{IMG_H}" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{data}"/>
{chr(10).join(decor)}
{chr(10).join(petals)}
</svg>
'''
open(out_path, "w").write(svg)
print(W, H, len(svg) // 1024, "KB")
