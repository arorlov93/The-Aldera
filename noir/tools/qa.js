// QA: раскадровка действия. node qa.js out.jpg x y w h t1 t2 ...
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [out, x, y, w, h, ...ts] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + __dirname + '/../' + (process.env.SCENE || 'scene_smoker_diner.html'));
  const files = [];
  for (const t of ts) { const d = await p.evaluate(t => window.frameJpeg(+t), t); const f = `qa_${t}.jpg`; fs.writeFileSync(f, Buffer.from(d.split(',')[1], 'base64')); files.push(f); }
  await b.close();
  fs.writeFileSync('qa_list.txt', JSON.stringify({ out, box: [+x, +y, +w, +h], files }));
})();
