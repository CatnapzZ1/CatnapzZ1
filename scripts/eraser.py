"""Vector eraser and rubbed-off shavings used by interlude.py."""
# a soft, vector eraser that matches the sakura style: rubber end + striped paper sleeve
L, HGT = 64, 22          # body length and height (local coords, centred on the origin)
SLEEVE_X = -L / 2 + 22   # where the sleeve starts

def eraser(x, y, rot=-12, shadow=True, rub=True):
    x0, y0 = -L / 2, -HGT / 2
    # the rubber end is worn round on the erasing side
    body = (f"M{x0 + 6} {y0}H{-x0}V{-y0}H{x0 + 6}"
            f"C{x0 + 1} {-y0} {x0 - 1} {y0 + HGT * 0.7} {x0} {y0 + HGT * 0.5}"
            f"C{x0 - 1} {y0 + HGT * 0.3} {x0 + 1} {y0} {x0 + 6} {y0}Z")
    sx, sw = SLEEVE_X, -x0 - SLEEVE_X
    stripes = (
        f'<rect x="{sx}" y="{y0 - 1}" width="{sw * 0.55}" height="{HGT + 2}" fill="url(#sleeve-blue)"/>'
        f'<rect x="{sx + sw * 0.55}" y="{y0 - 1}" width="{sw * 0.17}" height="{HGT + 2}" fill="#ffffff"/>'
        f'<rect x="{sx + sw * 0.72}" y="{y0 - 1}" width="{sw * 0.28}" height="{HGT + 2}" fill="#2f3a4f"/>'
    )
    out = []
    if shadow:
        out.append(f'<ellipse cx="{x + 2}" cy="{y + 15}" rx="{L * 0.48}" ry="4" fill="#57606a" opacity="0.18"/>')
    # rub back and forth along its own axis a couple of times, then rest
    import math
    ux, uy = math.cos(math.radians(rot)) * 3, math.sin(math.radians(rot)) * 3
    anim = (f'<animateTransform attributeName="transform" type="translate" additive="sum" dur="4.5s" repeatCount="indefinite" '
            f'values="0 0;{-ux:.2f} {-uy:.2f};0 0;{-ux:.2f} {-uy:.2f};0 0;0 0" keyTimes="0;0.07;0.14;0.21;0.28;1"/>') if rub else ""
    out.append(
        f'<g transform="translate({x} {y}) rotate({rot})">{anim}'
        f'<path d="{body}" fill="url(#rubber)" stroke="#8b949e" stroke-width="1"/>'
        # graphite picked up on the worn, erasing end
        f'<path d="{body}" fill="url(#graphite)"/>'
        # highlight along the top edge of the rubber gives it a little volume
        f'<path d="M{x0 + 6} {y0 + 2.5}H{sx}" stroke="#ffffff" stroke-width="2" stroke-linecap="round" opacity="0.9"/>'
        f'{stripes}'
        f'<rect x="{sx}" y="{y0 - 1}" width="{sw}" height="{HGT + 2}" rx="1.5" fill="none" stroke="#3d4757" stroke-width="1"/>'
        f'<rect x="{sx}" y="{y0 - 1}" width="{sw}" height="5" fill="#ffffff" opacity="0.18"/>'
        '</g>')
    return "".join(out)

DEFS = ('<linearGradient id="graphite" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#8b949e" stop-opacity="0.55"/><stop offset="0.12" stop-color="#8b949e" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="smudge"><stop offset="0" stop-color="#9aa4ae" stop-opacity="0.22"/>'
        '<stop offset="1" stop-color="#9aa4ae" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="rubber" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9e3e6"/></linearGradient>'
        '<linearGradient id="sleeve-blue" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#5b9be0"/><stop offset="1" stop-color="#2f64a6"/></linearGradient>')

def crumbs(points):
    # rubbed-off shavings: short curled rods with a darker underside
    out = []
    for cx, cy, length, rot in points:
        w = max(1.4, length * 0.32)
        out.append(
            f'<g transform="translate({cx} {cy}) rotate({rot})">'
            f'<path d="M{-length / 2:.1f} 0Q0 {-w * 0.5:.1f} {length / 2:.1f} 0" fill="none" stroke="#b3abb0" stroke-width="{w + 1:.1f}" stroke-linecap="round"/>'
            f'<path d="M{-length / 2:.1f} 0Q0 {-w * 0.5:.1f} {length / 2:.1f} 0" fill="none" stroke="#f6f2f4" stroke-width="{w:.1f}" stroke-linecap="round"/>'
            '</g>')
    return "".join(out)
