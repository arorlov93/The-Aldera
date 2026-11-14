// крупный план объекта в координатах улицы: node zoom.js out.jpg cx cy z t
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [out, cx, cy, z, t] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + __dirname + '/scene.html');
  const d = await p.evaluate(([cx, cy, z, t]) => { window.camera = () => [cx, cy, z]; window.draw(t); return document.getElementById('c').toDataURL('image/jpeg', 0.9); }, [+cx, +cy, +z, +t]);
  fs.writeFileSync(out, Buffer.from(d.split(',')[1], 'base64')); await b.close(); })();
