"""Рендер саше 30x50 мм без Blender: плоский макет + карта высот (подушка, рифлёные швы,
капсулы внутри) + освещение по нормалям. Запуск: python3 render_3x5.py
Вход: ../flat_art_3x5/mg_sfront.png, mg_sback.png (из art_3x5.html, 40 px/мм).
Выход: ../renders/sachet_3x5_mg.jpg"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', 'flat_art_3x5')
OUT = os.path.join(HERE, '..', 'renders', 'sachet_3x5_mg.jpg')

PPM = 26                       # пикселей на мм в сцене
SW, SH = 30.0, 50.0            # саше, мм
SIDE, TOP, BOT = 3.5, 5.0, 3.5 # швы, мм
CAP_L, CAP_D = 21.7, 7.6       # капсула размера 0, мм
LIGHT = np.array([-0.45, -0.65, 0.62]); LIGHT /= np.linalg.norm(LIGHT)


def box_blur(a, r):
    if r < 1:
        return a
    k = 2 * r + 1
    p = np.pad(a, ((r + 1, r), (0, 0)), mode='edge'); c = np.cumsum(p, 0); a = (c[k:] - c[:-k]) / k
    p = np.pad(a, ((0, 0), (r + 1, r)), mode='edge'); c = np.cumsum(p, 1); a = (c[:, k:] - c[:, :-k]) / k
    return a


def gblur(a, sigma_px):
    r = max(1, int(sigma_px * 0.9))
    for _ in range(3):
        a = box_blur(a, r)
    return a


def stadium_height(X, Y, cx, cy, length, dia, vertical=True):
    """Высота капсулы (полусфера по сечению) в мм, 0 вне капсулы."""
    r = dia / 2
    u, v = (Y - cy, X - cx) if vertical else (X - cx, Y - cy)
    half = length / 2 - r
    du = np.clip(np.abs(u) - half, 0, None)
    d = np.sqrt(du ** 2 + v ** 2)
    return np.where(d < r, np.sqrt(np.clip(r * r - d * d, 0, None)), 0.0)


def shade(albedo, h, spec=0.05, shin=30, amb=0.74, dif=0.36):
    gy, gx = np.gradient(h, 1.0 / PPM)
    n = np.dstack([-gx, -gy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    ndl = np.clip(n @ LIGHT, 0, None)
    half = LIGHT + np.array([0, 0, 1.0]); half /= np.linalg.norm(half)
    s = np.clip(n @ half, 0, None) ** shin * spec
    col = albedo * (amb + dif * ndl)[..., None] + s[..., None]
    return np.clip(col, 0, 1)


def make_sachet(art_path, with_caps=True):
    W, H = int(SW * PPM), int(SH * PPM)
    art = Image.open(art_path).convert('RGB')
    a = art.crop((2, 2, art.width - 2, art.height - 2)).resize((W, H), Image.LANCZOS)
    alb = np.asarray(a, dtype=np.float32) / 255.0
    y, x = np.mgrid[0:H, 0:W].astype(np.float32) / PPM
    # подушка: растёт от внутренней кромки швов
    dx = np.minimum(x - SIDE, SW - SIDE - x); dy = np.minimum(y - TOP, SH - BOT - y)
    inner = np.clip(np.minimum(dx, dy), 0, None)
    hgt = 0.75 * (1 - np.exp(-inner / 2.2))
    if with_caps:
        cy = TOP + (SH - TOP - BOT) / 2 + 0.6
        caps = np.maximum(stadium_height(x, y, SW / 2 - 4.1, cy, CAP_L, CAP_D),
                          stadium_height(x, y, SW / 2 + 4.1, cy, CAP_L, CAP_D))
        hgt = np.maximum(hgt, 0.22 * caps + 0.18 * (caps > 0))
    hgt = gblur(hgt, 1.3 * PPM)
    # рифление швов: рёбра поперёк кромки
    seal_side = (x < SIDE) | (x > SW - SIDE)
    seal_tb = (y < TOP) | (y > SH - BOT)
    rib_s = 0.025 * np.sin(2 * np.pi * y / 0.6)
    rib_t = 0.025 * np.sin(2 * np.pi * x / 0.6)
    hgt = hgt + np.where(seal_tb, rib_t, np.where(seal_side, rib_s, 0))
    col = shade(alb, hgt)
    # швы чуть темнее и матовее: две плёнки спаяны
    col = np.where((seal_side | seal_tb)[..., None], col * 0.97, col)
    # форма: зубчатый срез сверху и снизу, надсечки по бокам на линии отрыва
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    per, amp = 1.6 * PPM, 0.55 * PPM
    pts = [(0, amp)]
    for i in range(int(W / per) + 2):
        pts += [(min(W, i * per + per / 2), 0), (min(W, (i + 1) * per), amp)]
    for i in range(int(W / per) + 2, -1, -1):
        pts += [(min(W, (i + 1) * per), H - amp), (min(W, i * per + per / 2), H)]
    d.polygon(pts + [(0, H - amp)], fill=255)
    ty = 7.6 * PPM
    for side in (0, W):
        s = 1 if side == 0 else -1
        d.polygon([(side, ty - 0.6 * PPM), (side + s * 1.2 * PPM, ty), (side, ty + 0.6 * PPM)], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.fromarray((col * 255).astype(np.uint8)).convert('RGBA'); img.putalpha(m)
    return img


def make_capsule():
    L, D = int(CAP_L * PPM), int(CAP_D * PPM)
    y, x = np.mgrid[0:L, 0:D].astype(np.float32) / PPM
    h = stadium_height(x, y, CAP_D / 2, CAP_L / 2, CAP_L, CAP_D)
    alb = np.ones((L, D, 3), np.float32) * np.array([0.96, 0.94, 0.90])
    seam = np.abs(y - CAP_L * 0.56) < 0.12
    alb[seam] *= 0.9
    col = shade(alb, h * 1.0, spec=0.30, shin=60, amb=0.70, dif=0.40)
    m = Image.fromarray(((h > 0) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
    img = Image.fromarray((col * 255).astype(np.uint8)).convert('RGBA'); img.putalpha(m)
    return img


def place(canvas, sprite, xy, angle, shadow=(14, 22, 26, 0.32)):
    s = sprite.rotate(angle, resample=Image.BICUBIC, expand=True)
    ox, oy, blur, op = shadow
    sh = Image.new('RGBA', s.size, (60, 40, 30, 0)); a = s.split()[3].point(lambda v: int(v * op))
    sh.putalpha(a); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (xy[0] - s.width // 2 + ox, xy[1] - s.height // 2 + oy))
    canvas.alpha_composite(s, (xy[0] - s.width // 2, xy[1] - s.height // 2))


def background(W, H):
    rng = np.random.default_rng(7)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.array([0.905, 0.875, 0.835])
    g = 1.03 - 0.10 * ((x / W - 0.35) ** 2 + (y / H - 0.3) ** 2)
    n = gblur(rng.normal(0, 1, (H, W)).astype(np.float32), 2.0) * 0.015
    col = base * (g + n)[..., None]
    return Image.fromarray((np.clip(col, 0, 1) * 255).astype(np.uint8)).convert('RGBA')


def dim(d, p1, p2, label, font, col=(70, 40, 40, 255), vertical=False):
    d.line([p1, p2], fill=col, width=3)
    for p in (p1, p2):
        if vertical:
            d.line([(p[0] - 14, p[1]), (p[0] + 14, p[1])], fill=col, width=3)
        else:
            d.line([(p[0], p[1] - 14), (p[0], p[1] + 14)], fill=col, width=3)
    mx, my = (p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2
    tw = d.textlength(label, font=font)
    if vertical:
        d.rectangle([mx - tw / 2 - 10, my - 28, mx + tw / 2 + 10, my + 28], fill=(231, 223, 213, 255))
        d.text((mx - tw / 2, my - 24), label, font=font, fill=col)
    else:
        d.rectangle([mx - tw / 2 - 10, my - 28, mx + tw / 2 + 10, my + 28], fill=(231, 223, 213, 255))
        d.text((mx - tw / 2, my - 24), label, font=font, fill=col)


def main():
    W, H = 2600, 1700
    cv = background(W, H)
    front = make_sachet(os.path.join(ART, 'mg_sfront.png'))
    back = make_sachet(os.path.join(ART, 'mg_sback.png'))
    cap = make_capsule()
    fx, fy = 700, 860
    place(cv, front, (fx, fy), 0)
    place(cv, back, (1560, 880), -5)
    place(cv, cap, (2200, 760), -24, shadow=(8, 12, 10, 0.35))
    place(cv, cap, (2340, 930), -8, shadow=(8, 12, 10, 0.35))
    d = ImageDraw.Draw(cv)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 40)
        fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
    except OSError:
        f = fs = ImageFont.load_default()
    sw, sh = int(SW * PPM), int(SH * PPM)
    dim(d, (fx - sw // 2, fy + sh // 2 + 60), (fx + sw // 2, fy + sh // 2 + 60), '3 см', f)
    dim(d, (fx - sw // 2 - 70, fy - sh // 2), (fx - sw // 2 - 70, fy + sh // 2), '5 см', f, vertical=True)
    d.text((2040, 1110), 'капсулы размера 0, 2 шт.', font=fs, fill=(90, 60, 55, 255))
    d.text((60, 1640), 'The Aldera · Day Pass, саше 30 × 50 мм · визуализация для обсуждения, тексты-заглушки', font=fs, fill=(110, 80, 75, 255))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv.convert('RGB').save(OUT, quality=92)
    print(OUT)


if __name__ == '__main__':
    main()
