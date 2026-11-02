# One PDF for suppliers: sachet drawing, carton dieline, sachet artwork, look render (A3 landscape)
import asyncio, base64, pathlib
from playwright.async_api import async_playwright
R = pathlib.Path(__file__).resolve().parent.parent
def svg(p): return (R / p).read_text().replace('<svg ', '<svg preserveAspectRatio="xMidYMid meet" ', 1)
def img(p): return 'data:image/png;base64,' + base64.b64encode((R / p).read_bytes()).decode() if p.endswith('.png') else 'data:image/jpeg;base64,' + base64.b64encode((R / p).read_bytes()).decode()
def page(title, inner, note=''):
    return f'<section class="pg"><header><b>THE ALDERA</b> · 518 GROUP LLC · {title}</header><div class="art">{inner}</div><footer>{note}</footer></section>'
pages = [
    page('1 / 4 · Day Pass sachet 30 x 50 mm · shape drawing', svg('dielines/dieline_sachet_30x50.svg'),
         'Drawing at 2:1. Finished size 30 x 50 mm. All dimensions in mm.'),
    page('2 / 4 · 30-Day Pass carton for 30 x 50 mm sachets · dieline', svg('dielines/dieline_box_30x50.svg'),
         'Inner size 137 x 62 x 52 mm, to be confirmed with a filled sachet sample before printing.'),
    page('3 / 4 · Sachet artwork draft (Magnesium)',
         f'<div class="pair"><figure><img src="{img("flat_art_3x5/mg_sfront.png")}"><figcaption>FRONT</figcaption></figure>'
         f'<figure><img src="{img("flat_art_3x5/mg_sback.png")}"><figcaption>BACK</figcaption></figure></div>',
         'Design in development, texts are placeholders. 4 designs in total: same layout, one colour per product (Magnesium, Ashwagandha, Moringa, Shilajit).'),
    page('4 / 4 · Planned look (render)', f'<img class="photo" src="{img("renders/hero_mg.jpg")}">',
         'Render for reference only. Final carton follows the dieline on page 2.'),
]
html = '''<!doctype html><html><head><meta charset="utf-8"><style>
@page{size:420mm 297mm; margin:0}
body{margin:0; font-family:Arial, sans-serif; color:#222}
.pg{width:420mm; height:297mm; box-sizing:border-box; padding:12mm 14mm; display:flex; flex-direction:column; page-break-after:always}
header{font-size:11pt; border-bottom:.4mm solid #4A1424; padding-bottom:3mm; color:#4A1424}
footer{font-size:9.5pt; color:#555; border-top:.2mm solid #ccc; padding-top:3mm}
.art{flex:1; min-height:0; display:flex; align-items:center; justify-content:center; padding:6mm 0}
.art > svg{width:100%; height:100%}
.pair{display:flex; gap:20mm; height:100%; align-items:center}
.pair figure{margin:0; height:85%; display:flex; flex-direction:column; align-items:center}
.pair img{height:100%; border:.2mm solid #ddd}
figcaption{font-size:10pt; letter-spacing:.2em; margin-top:3mm}
.photo{max-height:100%; max-width:100%; object-fit:contain}
</style></head><body>''' + ''.join(pages) + '</body></html>'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless', '--no-sandbox'])
        pg = await b.new_page()
        await pg.set_content(html)
        await pg.pdf(path=str(R / 'The Aldera - Day Pass sachet and carton 30x50.pdf'), width='420mm', height='297mm', print_background=True)
        await b.close()
asyncio.run(main())
print('ok')
