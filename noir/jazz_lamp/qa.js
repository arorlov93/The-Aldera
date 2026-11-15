// Раскадровка: node qa.js out.jpg t1 t2 ...  (кадры 270x480 в одну ленту)
const { chromium } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process');
(async () => { const [out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + __dirname + '/scene.html'); const files = [];
  for (const t of ts) { const d = await p.evaluate(t => window.frameJpeg(+t), t); const f = `/tmp/qa_${t}.jpg`; fs.writeFileSync(f, Buffer.from(d.split(',')[1], 'base64')); files.push(f); }
  await b.close();
  execSync(`python3 -c "from PIL import Image,ImageDraw;fs='${files.join(' ')}'.split();o=Image.new('RGB',(270*len(fs),480));[ (lambda im,i:(ImageDraw.Draw(im).text((5,5),fs[i].split('_')[-1][:-4],fill='yellow'),o.paste(im,(270*i,0))))(Image.open(f).resize((270,480)),i) for i,f in enumerate(fs)];o.save('${out}')"`);
})();
