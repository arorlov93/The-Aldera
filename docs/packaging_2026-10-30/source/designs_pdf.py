# One A3 page: front and back of the 30 x 50 mm sachet for all 4 products
import asyncio, base64, pathlib
from playwright.async_api import async_playwright
R = pathlib.Path(__file__).resolve().parent.parent
names = {'mg': 'Magnesium', 'ashwa': 'Ashwagandha', 'moringa': 'Moringa', 'shilajit': 'Shilajit'}
def img(p): return 'data:image/png;base64,' + base64.b64encode((R / p).read_bytes()).decode()
cols = ''.join(f'<div class="col"><h3>{n}</h3><div class="pair"><img src="{img(f"flat_art_3x5/{k}_sfront.png")}"><img src="{img(f"flat_art_3x5/{k}_sback.png")}"></div><p>FRONT · BACK</p></div>' for k, n in names.items())
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:420mm 297mm; margin:0}} body{{margin:0; font-family:Arial, sans-serif; color:#222}}
.pg{{width:420mm; height:297mm; box-sizing:border-box; padding:12mm 14mm; display:flex; flex-direction:column}}
header{{font-size:11pt; border-bottom:.4mm solid #4A1424; padding-bottom:3mm; color:#4A1424}}
.grid{{flex:1; display:grid; grid-template-columns:repeat(4,1fr); gap:8mm; align-items:center}}
.col h3{{font-size:12pt; margin:0 0 4mm; text-align:center}} .pair{{display:flex; gap:3mm; justify-content:center}}
.pair img{{width:40mm; border:.2mm solid #ccc}} .col p{{text-align:center; font-size:8pt; letter-spacing:.2em; color:#666}}
footer{{font-size:9.5pt; color:#555; border-top:.2mm solid #ccc; padding-top:3mm}}
</style></head><body><section class="pg"><header><b>THE ALDERA</b> · 518 GROUP LLC · Day Pass sachet 30 x 50 mm · 4 designs (draft)</header>
<div class="grid">{cols}</div><footer>Shown larger than actual size. Same layout for all 4 products, only the colour and product name change. Design in development, texts are placeholders. Final artwork before printing.</footer></section></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless', '--no-sandbox'])
        pg = await b.new_page(); await pg.set_content(html)
        await pg.pdf(path=str(R / 'The Aldera - Day Pass sachet 4 designs.pdf'), width='420mm', height='297mm', print_background=True)
        await b.close()
asyncio.run(main()); print('ok')
