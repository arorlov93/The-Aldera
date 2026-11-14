import json
from PIL import Image, ImageDraw
c = json.load(open('qa_list.txt')); x, y, w, h = c['box']
ims = [Image.open(f).crop((x, y, x + w, y + h)) for f in c['files']]
sc = min(1.0, 2400 / (len(ims) * (w + 6)))
W = int(w * sc); H = int(h * sc)
S = Image.new('RGB', (len(ims) * (W + 6), H + 30), 'black'); d = ImageDraw.Draw(S)
for i, (im, f) in enumerate(zip(ims, c['files'])):
    S.paste(im.resize((W, H)), (i * (W + 6), 30)); d.text((i * (W + 6) + 4, 8), f[3:-4], fill='white')
S.save(c['out'])
