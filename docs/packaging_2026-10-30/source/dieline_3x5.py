# Day Pass sachet 30 x 50 mm: shape drawing (front, side profile, section A-A), scale 2:1
import asyncio
from playwright.async_api import async_playwright

CUT, SEAL, DIM, SAFE = '#C0143C', '#000', '#555', '#2E8B57'
K = 2  # drawing scale 2:1
DASH = 'stroke-dasharray="1.2 0.8"'

def line(x1, y1, x2, y2, c=DIM, dash=False, w=.3): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" {DASH if dash else ""}/>'
def text(x, y, t, s=3, c=DIM, a='middle', wt='normal', rot=None):
    r = f' transform="rotate(-90 {x} {y})"' if rot else ''
    return f'<text x="{x}" y="{y}" font-size="{s}" fill="{c}" text-anchor="{a}" font-weight="{wt}"{r}>{t}</text>'
def dimh(x1, x2, y, lab): return line(x1, y, x2, y, w=.2) + line(x1, y-1.5, x1, y+1.5, w=.2) + line(x2, y-1.5, x2, y+1.5, w=.2) + text((x1+x2)/2, y-1.2, lab, 2.8)
def dimv(x, y1, y2, lab): return line(x, y1, x, y2, w=.2) + line(x-1.5, y1, x+1.5, y1, w=.2) + line(x-1.5, y2, x+1.5, y2, w=.2) + text(x-1.3, (y1+y2)/2, lab, 2.8, rot=True)
def zig(x1, x2, y, amp, step=1.6):
    pts, x, up = [], x1, True
    while x <= x2 + 1e-6:
        pts.append((x, y - amp if up else y)); x += step/2; up = not up
    return pts

SW, SH = 30, 50          # finished size, mm
SIDE, TOP, BOT = 3, 6, 5  # seal widths, mm
NOTCH = 9                 # tear notch from top, mm
CAP_L, CAP_D = 23.3, 8.5  # capsule size 00

def front(x0, y0, label):
    w, h = SW*K, SH*K
    o = ''
    top = zig(x0, x0+w, y0+1.2*K, 1.2*K)
    bot = zig(x0, x0+w, y0+h, -1.2*K)
    outline = [(x0, y0+1.2*K)] + top + [(x0+w, y0+h-1.2*K)] + list(reversed(bot)) + [(x0, y0+1.2*K)]
    o += f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in outline)}" fill="#FBF7F0" stroke="{CUT}" stroke-width=".4"/>'
    for r in [(x0, y0, w, TOP*K), (x0, y0+h-BOT*K, w, BOT*K), (x0, y0, SIDE*K, h), (x0+w-SIDE*K, y0, SIDE*K, h)]:
        o += f'<rect x="{r[0]}" y="{r[1]}" width="{r[2]}" height="{r[3]}" fill="{SEAL}" opacity=".08"/>'
    o += f'<rect x="{x0+(SIDE+2)*K}" y="{y0+(TOP+2)*K}" width="{(SW-2*SIDE-4)*K}" height="{(SH-TOP-BOT-4)*K}" fill="none" stroke="{SAFE}" stroke-width=".25" {DASH}/>'
    ny = y0 + NOTCH*K
    o += f'<polygon points="{x0},{ny-1.5} {x0+2.4},{ny} {x0},{ny+1.5}" fill="#fff" stroke="{CUT}" stroke-width=".35"/>'
    o += f'<polygon points="{x0+w},{ny-1.5} {x0+w-2.4},{ny} {x0+w},{ny+1.5}" fill="#fff" stroke="{CUT}" stroke-width=".35"/>'
    o += line(x0+2.4, ny, x0+w-2.4, ny, DIM, True, .25)
    cy = y0 + (TOP + (SH-TOP-BOT)/2)*K
    for cx in (x0 + w/2 - (CAP_D/2+0.6)*K, x0 + w/2 + (CAP_D/2+0.6)*K):
        o += f'<rect x="{cx-CAP_D/2*K}" y="{cy-CAP_L/2*K}" width="{CAP_D*K}" height="{CAP_L*K}" rx="{CAP_D/2*K}" fill="#fff" stroke="#999" stroke-width=".3" {DASH}/>'
        o += line(cx-CAP_D/2*K+1, cy+1.5*K, cx+CAP_D/2*K-1, cy+1.5*K, '#bbb', False, .25)
    o += text(x0+w/2, y0-6, label, 3.6, '#111', wt='bold')
    return o

def side(x0, y0):
    h, t = SH*K, 9.5*K
    o = text(x0, y0-6, 'SIDE PROFILE', 3.6, '#111', wt='bold')
    cx = x0
    o += f'<path d="M{cx},{y0} L{cx},{y0+TOP*K} C{cx+t*0.55},{y0+(TOP+6)*K} {cx+t*0.55},{y0+h-(BOT+6)*K} {cx},{y0+h-BOT*K} L{cx},{y0+h} M{cx},{y0+TOP*K} C{cx-t*0.55},{y0+(TOP+6)*K} {cx-t*0.55},{y0+h-(BOT+6)*K} {cx},{y0+h-BOT*K}" fill="#FBF7F0" stroke="{CUT}" stroke-width=".4"/>'
    o += line(cx, y0, cx, y0+TOP*K, CUT, False, 1.1) + line(cx, y0+h-BOT*K, cx, y0+h, CUT, False, 1.1)
    o += dimh(cx-t/2*1.05, cx+t/2*1.05, y0+h+8, '≈ 9-10 filled')
    return o

def section(x0, y0):
    o = text(x0+SW*K/2, y0-6, 'SECTION A-A', 3.6, '#111', wt='bold')
    w_in = (SW-2*SIDE)*K
    t = 9.5*K
    xa, xb, yc = x0+SIDE*K, x0+SW*K-SIDE*K, y0+t/2
    o += f'<path d="M{x0},{yc} L{xa},{yc} C{xa+4},{yc-t*0.66} {xb-4},{yc-t*0.66} {xb},{yc} L{x0+SW*K},{yc} M{xa},{yc} C{xa+4},{yc+t*0.66} {xb-4},{yc+t*0.66} {xb},{yc}" fill="#FBF7F0" stroke="{CUT}" stroke-width=".4"/>'
    r = CAP_D/2*K
    for cx in (x0+SW*K/2-r-0.5, x0+SW*K/2+r+0.5):
        o += f'<circle cx="{cx}" cy="{yc}" r="{r}" fill="#fff" stroke="#999" stroke-width=".3"/>'
    o += dimh(x0, x0+SW*K, y0+t+9, '30')
    return o

x0, y0 = 26, 78
s = ''
s += front(x0, y0, 'FRONT') + front(x0+92, y0, 'BACK')
s += dimh(x0, x0+SW*K, y0+SH*K+9, '30') + dimv(x0-8, y0, y0+SH*K, '50')
s += dimv(x0+SW*K+6, y0, y0+TOP*K, '6') + dimv(x0+SW*K+6, y0+SH*K-BOT*K, y0+SH*K, '5') + dimh(x0, x0+SIDE*K, y0+SH*K+17, '3')
s += dimv(x0+SW*K+14, y0, y0+NOTCH*K, '9')
s += text(x0+SW*K+16, y0+NOTCH*K+1, 'tear notch', 2.6, CUT, 'start')
s += line(x0-3, y0+(TOP+(SH-TOP-BOT)/2)*K, x0+SW*K+3, y0+(TOP+(SH-TOP-BOT)/2)*K, '#888', True, .2) + text(x0-4, y0+(TOP+(SH-TOP-BOT)/2)*K+1, 'A', 3, '#111', 'end', 'bold')
s += side(x0+180, y0) + section(x0+196, y0+10)

s += text(20, 16, 'THE ALDERA · Day Pass sachet · shape drawing · scale 2:1', 5.2, '#111', 'start', 'bold')
notes = [
    'Finished size 30 x 50 mm, flat 3-side seal (fin seal on sides, top seal after filling) · serrated cut top and bottom',
    'Seals: sides 3 mm, top 6 mm, bottom 5 mm · inner pocket 24 x 39 mm · tear notches both sides, 9 mm from top',
    'Contents: 2 capsules size 00 (23.3 x 8.5 mm) · filled thickness about 9-10 mm · capsules lie side by side or stacked',
    'Laminate: matte PET 12 / AL foil 7 / PE 50 µm (moisture barrier) · print both sides · LOT / EXP printed on the back',
]
for i, n in enumerate(notes):
    s += text(20, 25 + i*6, n, 3.2, '#333', 'start')
for i, (c, d, t) in enumerate([(CUT, False, 'cut / outline'), (SEAL, False, 'grey: seal zone, no small text'), (SAFE, True, 'safe area for text'), (DIM, True, 'tear line')]):
    s += line(20+i*62, 55, 30+i*62, 55, c if c != SEAL else '#bbb', d, .7 if c != SEAL else 2.2) + text(33+i*62, 56.2, t, 3, '#333', 'start')
s += text(20, 205, 'Capsule check: two size 00 capsules need about 44 mm of film around them; the 24 mm pocket gives 48 mm. Size 0 capsules fit with more room.', 3, '#333', 'start')

W, H = 290, 212
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" font-family="Arial"><rect width="100%" height="100%" fill="#fff"/>{s}</svg>'
open('../dielines/dieline_sachet_30x50.svg', 'w').write(svg)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless', '--no-sandbox'])
        pg = await b.new_page(viewport={'width': 1450, 'height': 1060}, device_scale_factor=2)
        px = svg.replace(f'width="{W}mm" height="{H}mm"', 'width="1450" height="1060"')
        await pg.set_content('<html><body style="margin:0">' + px + '</body></html>')
        await pg.screenshot(path='../dielines/dieline_sachet_30x50.png', clip={'x': 0, 'y': 0, 'width': 1450, 'height': 1060})
        await pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
        await pg.pdf(path='../dielines/dieline_sachet_30x50.pdf', width=f'{W}mm', height=f'{H}mm', print_background=True)
        await b.close()

asyncio.run(main())
print('ok')
