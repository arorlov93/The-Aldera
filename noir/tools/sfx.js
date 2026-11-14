const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + __dirname + '/scene.html'); const ev = await p.evaluate(() => window.sfxEvents());
  fs.writeFileSync('sfx.json', JSON.stringify(ev)); console.log(ev.length, JSON.stringify(ev.slice(-4))); await b.close(); })();
