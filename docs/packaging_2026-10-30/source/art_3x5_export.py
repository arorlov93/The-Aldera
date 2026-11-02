# Export 30 x 50 mm sachet flat art for every product at 40 px/mm (same scale as mg_*.png)
import asyncio, pathlib
from playwright.async_api import async_playwright
R = pathlib.Path(__file__).resolve().parent
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless', '--no-sandbox'])
        pg = await b.new_page(device_scale_factor=40 / 3.7795)
        for k in ['ashwa', 'moringa', 'shilajit']:
            await pg.goto((R / 'art_3x5.html').as_uri() + '?p=' + k, wait_until='networkidle')
            await pg.evaluate('document.fonts.ready')
            for side in ['sfront', 'sback']:
                await pg.locator('#' + side).screenshot(path=str(R.parent / 'flat_art_3x5' / f'{k}_{side}.png'))
        await b.close()
asyncio.run(main())
print('ok')
