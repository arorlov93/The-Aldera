"""The Aldera: positioning and final 4 SKUs (HTML -> PDF). Numbers: finmodel/twin.py and creators/suitable.json."""
import json, subprocess, sys, os, statistics
sys.path.insert(0,'finmodel')
from twin import PROD, FIX
S=json.load(open('creators/suitable.json'))
INK='#18211E'; MUT='#5A6762'; LINE='#D6DDD8'; ACC='#2C6A55'
def tbl(head,rows,num=set()):
    h='<table><thead><tr>'+''.join(f'<th class="{"n" if i in num else ""}">{x}</th>' for i,x in enumerate(head))+'</tr></thead><tbody>'
    for r in rows: h+='<tr>'+''.join(f'<td class="{"n" if i in num else ""}">{x}</td>' for i,x in enumerate(r))+'</tr>'
    return h+'</tbody></table>'
TTV=FIX['tt_fee']+FIX['cr_pct']+FIX['tt_ret']; PPC=0.15
def u(s):
    p=PROD[s]; c=p['p'][3]
    tt=p['ret']-c-p['ret']*TTV-p['sh']-2.5; sh=p['ret']-c-p['ret']*.049-.30-p['sh']-2.5; az=p['ret']-c-p['ret']*(.15+PPC)-p['fba']
    return p['ret'],c,tt,sh,az
cnt={k:sum(1 for m in S if m['lane']==k) for k in ('Колострум','Пробиотик','Магний','Креатин','Рутина')}
SKU=[('COL','Colostrum','14721','GUT','2,000 mg colostrum · 400 mg IgG','30 порций, порошок','Колострум'),
     ('PRO',"Women's Probiotic",'14648','BALANCE','50 Billion CFU','60 капсул','Пробиотик'),
     ('MG','Magnesium Glycinate','14683','REST','100% magnesium glycinate','90 капсул','Магний'),
     ('CRE','Creatine','14589','STRENGTH','5 g creatine monohydrate','60 порций, порошок','Креатин')]
sku_rows=[]
for s,n,art,role,num,fmt,lane in SKU:
    ret,c,tt,sh,az=u(s)
    sku_rows.append([f'<b>{n}</b><br><span class="mut">Vox {art} · {fmt}</span>',role,num,f'${ret:.2f}',f'${c:.2f}',f'${tt:.2f} · {tt/ret*100:.0f}%',f'${sh:.2f} · {sh/ret*100:.0f}%',f'${az:.2f} · {az/ret*100:.0f}%',str(cnt[lane])])
WHY=[['Colostrum','одна из самых быстрорастущих категорий TikTok Shop; ARMRA построил её одной цифрой IgG; на TikTok Shop уже продают Cowboy Colostrum, Prelude, Mentor, Magic Milk','спецификация Vox подписана, Prop 65 на макете нет','утро, кишечник, кофе'],
     ["Women's Probiotic",'женщины это основная аудитория покупателей добавок в TikTok Shop; там же активно продают Happy V, O Positiv, Physician\'s Choice, Love Wellness','живые культуры, нет типичного риска по свинцу','баланс, женское здоровье'],
     ['Magnesium Glycinate','одна из главных категорий Amazon; в TikTok Shop продают Double Wood, Doctor\'s Best, Carlyle; сон это массовая тема: 146 роликов про сон в нашей выборке','чистый глицинат, без оксида','вечер, сон, спокойствие'],
     ['Creatine','вторая волна спроса: креатин для женщин. В TikTok Shop креатин Wellah Pump-It-Up: больше 178 000 продаж, 34 598 отзывов, 4.6 звезды','креатинин в сырье не выше 100 ppm','сила, утро, тренировка']]
REJ=[['Электролит Vox 14703','на макете предупреждение Prop 65 о свинце'],['Ашваганда Vox 13066','Prop 65 «Reproductive Harm» на макете, микробиология до 10 млн КОЕ/г'],['Magnesium Complex 14668','40% магния из оксида, глицината 0,4%'],['Greens, Sea Moss','риск тяжёлых металлов, у Vox нет спецификации'],['Omega 3, Collagen','после комиссий TikTok прибыли почти не остаётся'],['GLP1, Berberine, Blood Sugar','категория держится на заявлениях о болезни']]
CSS=f'''@page{{size:A4;margin:15mm 14mm 16mm 14mm}}*{{box-sizing:border-box}}html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:"DejaVu Sans",sans-serif;font-size:8.8pt;line-height:1.45;color:{INK};margin:0}}
h1{{font-family:"DejaVu Serif",serif;font-size:23pt;line-height:1.12;margin:0 0 6pt}}h2{{font-family:"DejaVu Serif",serif;font-size:14pt;margin:16pt 0 6pt;color:{ACC};border-bottom:.8pt solid {ACC};padding-bottom:3pt;page-break-after:avoid}}
h3{{font-size:9.8pt;margin:10pt 0 4pt;page-break-after:avoid}}p{{margin:0 0 5pt}}.kicker{{font-size:7.4pt;letter-spacing:.14em;text-transform:uppercase;color:{MUT};font-weight:bold}}
table{{width:100%;border-collapse:collapse;margin:3pt 0 8pt;font-size:7.9pt;page-break-inside:avoid}}th{{background:#E2EEE8;text-align:left;padding:3.5pt 4pt;border-bottom:.8pt solid {ACC};vertical-align:bottom}}
td{{padding:3.2pt 4pt;border-bottom:.5pt solid {LINE};vertical-align:top}}td.n,th.n{{text-align:right;white-space:nowrap;font-family:"DejaVu Sans Mono",monospace}}.mut{{color:{MUT};font-size:7.4pt}}
.jars{{display:grid;grid-template-columns:repeat(4,1fr);gap:6pt;margin:6pt 0 8pt}}.jar{{border:.8pt solid {LINE};padding:8pt}}.jar .b{{font-size:6.6pt;letter-spacing:.2em;color:{MUT};font-weight:bold}}
.jar .r{{font-family:"DejaVu Sans Mono",monospace;font-size:7pt;letter-spacing:.12em;color:{ACC}}}.jar .nm{{font-family:"DejaVu Serif",serif;font-size:10.5pt;font-weight:bold;margin:2pt 0}}
.jar .big{{font-family:"DejaVu Sans Mono",monospace;font-size:8.4pt;border-top:.6pt solid {LINE};padding-top:4pt;margin-top:4pt}}.promise{{font-family:"DejaVu Serif",serif;font-size:17pt;margin:4pt 0 6pt}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:14pt}}ul{{margin:0 0 6pt;padding-left:14pt}}li{{margin-bottom:2pt}}.callout{{border-left:2.4pt solid #D08A2E;background:#FBF1E4;padding:6pt 9pt;margin:6pt 0 9pt}}
.foot{{font-size:7pt;color:{MUT};border-top:.5pt solid {LINE};padding-top:5pt;margin-top:12pt}}'''
jars=''.join(f'<div class="jar"><div class="b">THE ALDERA</div><div class="r">{role}</div><div class="nm">{n}</div><div class="big">{num}</div><div class="mut">${PROD[s]["ret"]:.2f} · {fmt}</div></div>' for s,n,art,role,num,fmt,lane in SKU)
html=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>The Aldera: позиционирование и 4 продукта</title><style>{CSS}</style></head><body>
<div class="kicker">The Aldera · 518 GROUP LLC · 03.10.2026</div>
<h1>Позиционирование и 4 продукта, которые мы продаём</h1>
<p>Итоговое решение по линейке и бренду. Производитель всех четырёх: Vox Nutrition (Юта), товар на складе, этикетка копирует макет завода, меняются только имя бренда и строка Distributed by 518 GROUP LLC.</p>
<h2>1. Четыре продукта</h2>
<div class="jars">{jars}</div>
{tbl(['Продукт','Роль','Цифра на банке','Розница','Банка @1 000','Прибыль TikTok','Прибыль Shopify','Прибыль Amazon','Криейторов под тему'],sku_rows,num={3,4,5,6,7,8})}
<p class="mut">Прибыль с одной банки после товара, комиссии TikTok 8%, криейтора 30%, доставки, склада $2.50 и возвратов; Amazon после 15% комиссии, FBA и рекламы 15% цены. Криейторов под тему: из 527 подходящих, проанализированных 03.10.</p>
<h3>Почему именно эти четыре</h3>
{tbl(['Продукт','Спрос','Риск по документам','Момент дня'],WHY)}
<h3>Что не продаём</h3>
{tbl(['Кандидат','Причина'],REJ)}
<h2>2. Позиционирование</h2>
<div class="promise">Four basics. Nothing to decode.</div>
<p>Четыре базовых продукта, нечего расшифровывать. Под мастер-теглайном платформы бренда: <b>What you see is what you get.</b></p>
<div class="two"><div>
<h3>Для кого</h3><p>Женщина 25-45, покупает добавки в TikTok Shop и на Amazon. Устала от банок с 20 ингредиентами и обещаниями, которые нечем проверить. Хочет базовые вещи, понятные с первого взгляда. Упаковка нейтральная: креатин и магний берут и мужчины, но голос бренда и криейторы женские.</p>
<h3>Чем отличаемся</h3><p>Рынок продаёт обещанием «моя жизнь изменилась». The Aldera продаёт цифрой: одно число крупно на лицевой стороне банки и то же число на обороте. Спокойная уверенность вместо хайпа.</p>
</div><div>
<h3>Ритуал дня</h3><ul><li><b>Утро:</b> Colostrum, Women's Probiotic, Creatine</li><li><b>Вечер:</b> Magnesium Glycinate</li></ul>
<h3>Цена в рынке</h3>{tbl(['Сегмент','Цена банки','Что продаёт'],[['Массовый Amazon','$15-25','цену за количество'],['<b>The Aldera</b>','<b>$30-40</b>','<b>проверяемую цифру</b>'],['Премиальный DTC','$50-100+','историю и обещание']],num={1})}
</div></div>
<h3>Наборы и подписка</h3>
{tbl(['Набор','Состав','Цена разово','Подписка в месяц'],[['Foundation','Colostrum + Magnesium','$59.95','$54.95'],['Gut Duo','Colostrum + Probiotic','$64.95','$59.95'],['The Daily Four','все четыре','$114.95','$99.95']],num={2,3})}
<h3>Голос бренда</h3>
{tbl(['Говорим','Не говорим'],[['clear, inside, purpose, what belongs, considered, simple','miracle, revolutionary, ultimate, detox, secret, breakthrough, hacked'],['что в банке и почему оно там','что продукт лечит, исцеляет, «меняет жизнь»'],['цифры с панели Supplement Facts','обещания результата за N дней']])}
<h2>3. Что показали данные по криейторам</h2>
<div class="callout">По 527 подходящим криейторам: ролик про продукт набирает в среднем <b>74%</b> от обычного ролика того же автора. Позиционирование, которое не выглядит как реклама, поэтому важно: чем ближе ролик к обычному контенту автора, тем меньше он теряет.</div>
{tbl(['Формат ролика','Суть','Почему работает'],[['<b>Flip the jar</b>','15 секунд: цифра спереди, переворот, та же цифра на обороте','короткий, нативный, сразу показывает отличие'],['Утренняя рутина','три банки утром, магний вечером','рутины это массовый жанр, продукт внутри, а не поверх'],['«Я убрала лишнее»','было девять банок, стало четыре понятные','спор с перегруженным рынком, наш главный смысл'],['Сон и вечер','магний в вечернем ритуале','сон: 146 роликов в выборке, одна из самых частых тем']])}
<p>Под каждый продукт найдено от 50 до 140 подходящих криейторов, то есть линейка не упрётся в нехватку авторов.</p>
<div class="foot">Источники: прайс и спецификации Vox Nutrition; финансовая модель finmodel/Aldera_FinModel.xlsx; анализ криейторов creators/Aldera_Creators_527.xlsx (публичные страницы TikTok, 03.10.2026); TikTok Shop (страницы товаров Wellah Pump-It-Up, Happy V, O Positiv, Physician's Choice, Cowboy Colostrum). Платформа бренда от 10.09.</div>
</body></html>'''
open('/tmp/pos.html','w').write(html)
out='docs/pdf/The Aldera - Positioning and 4 SKU.pdf'
subprocess.run(['/opt/pw-browsers/chromium-1194/chrome-linux/chrome','--headless','--no-sandbox','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={out}','/tmp/pos.html'],capture_output=True)
print('ok',os.path.getsize(out))
