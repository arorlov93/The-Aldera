from model_daily_four_amz import *
import html
NAMES={'COL':'Colostrum','PRO':"Women's Probiotic",'MG':'Magnesium Glycinate','CRE':'Creatine'}
ART={'COL':'14721','PRO':'14648','MG':'14683','CRE':'14589'}
ORDER=['COL','PRO','MG','CRE']
def M(v,dec=0):
    s=f"{abs(v):,.{dec}f}".replace(',',' ')
    return ('−$' if v<0 else '$')+s
def N(v): return f"{v:,.0f}".replace(',',' ')
def K(v):
    return f"${v/1e6:.2f} млн".replace('.',',') if abs(v)>=1e6 else f"${v/1e3:.0f} тыс."
def tbl(head,rows,cls='',numcols=None,total_rows=()):
    numcols=numcols or set(range(1,len(head)))
    h='<table class="%s"><thead><tr>'%cls+''.join('<th class="%s">%s</th>'%('n' if i in numcols else '',x) for i,x in enumerate(head))+'</tr></thead><tbody>'
    for ri,r in enumerate(rows):
        h+='<tr class="%s">'%('total' if ri in total_rows else '')+''.join('<td class="%s">%s</td>'%('n' if i in numcols else '',x) for i,x in enumerate(r))+'</tr>'
    return h+'</tbody></table>'

P=AMZSTD; o=run(P,FIRSTBUY); ob=run(STD,FIRSTBUY)
def ysum(o,a,b):
    rs=o[a:b]
    return dict(rev={k:sum(r['rev'][k] for r in rs) for k in ('tt','sh','az')},profit=sum(r['profit'] for r in rs),
      orders={k:sum(r['orders'][k] for r in rs) for k in ('tt','sh_first','sh_sub','az')},buy=sum(r['buy'] for r in rs),
      sku_rev={s:sum(r['sku_rev'][s] for r in rs) for s in SKUS},sku_prof={s:sum(r['sku_prof'][s] for r in rs) for s in SKUS},
      sku_ch={s:{c:sum(r['sku_ch'][s][c] for r in rs) for c in ('tt','sh','az')} for s in SKUS},
      goods=sum(r['goods'] for r in rs),platform=sum(r['platform'] for r in rs),creator=sum(r['creator'] for r in rs),
      ship=sum(r['ship'] for r in rs),returns=sum(r['returns'] for r in rs),ppc=sum(r['ppc'] for r in rs),fixed=sum(r['fixed'] for r in rs),
      lost=sum(r['lost'] for r in rs),subs=rs[-1]['subs_end'],cash=rs[-1]['cash'],
      videos=sum(r['videos'] for r in rs))
Y1=ysum(o,0,12); Y2=ysum(o,12,24); B1=ysum(ob,0,12); B2=ysum(ob,12,24)
QN=['Q1 · 20.11.26-31.01.27','Q2 · фев-апр 27','Q3 · май-июл 27','Q4 · авг-окт 27','Q5 · ноя 27-янв 28','Q6 · фев-апр 28','Q7 · май-июл 28','Q8 · авг-окт 28']
Q=[ysum(o,i*3,i*3+3) for i in range(8)]
hit=next(r['m'] for r in o if r['profit']*12>=1e6)
MON=['ноябрь 2026','декабрь 2026','январь 2027','февраль 2027','март 2027','апрель 2027','май 2027','июнь 2027','июль 2027','август 2027','сентябрь 2027','октябрь 2027']

# unit economics per product (single jar), with fulfilment 2.50, tier 1000 and 5000
def unit(s,c):
    p=RET[s]
    tt=p-c-p*(.06+.30+.03)-SHIP[s]-2.5
    sh=p-c-(p*(.029+.02)+.30)-SHIP[s]-2.5
    az=p-c-.15*p-FBA[s]-P['ppc']*p
    return tt,sh,az
first_cost={s:tier_cost(s,FIRSTBUY[s]) for s in SKUS}
rows=[]
for s in ORDER:
    c1=tier_cost(s,1000); c5=tier_cost(s,5000)
    tt,sh,az=unit(s,c1)
    rows.append([f"<b>{NAMES[s]}</b><br><span class='mut'>Vox {ART[s]}</span>",M(first_cost[s],2),M(c1,2),M(c5,2),M(RET[s],2),
                 f"{M(tt,2)}<br><span class='mut'>{tt/RET[s]*100:.0f}%</span>",f"{M(sh,2)}<br><span class='mut'>{sh/RET[s]*100:.0f}%</span>",f"{M(az,2)}<br><span class='mut'>{az/RET[s]*100:.0f}%</span>"])
unit_tbl=tbl(['Продукт','Банка в 1-й закупке','Банка @1 000','Банка @5 000','Розница','Прибыль TikTok','Прибыль Shopify','Прибыль Amazon'],rows)

# first purchase
fp_rows=[]; tot=0
for s in ['COL','MG','PRO','CRE']:
    c=first_cost[s]; v=FIRSTBUY[s]*c; tot+=v
    fp_rows.append([f"{NAMES[s]} {ART[s]}",N(FIRSTBUY[s]),M(c,2),M(v),M(FIRSTBUY[s]*RET[s]),M(FIRSTBUY[s]*unit(s,c)[0])])
fp_rows+= [['Дизайн 4 этикеток','','',M(499),'',''],['GS1, лицензия и 4 GTIN','','',M(300),'',''],['Фрахт Юта, Авентура','','',M(500),'',''],['Образцы 50 криейторам','','',M(950),'','']]
fp_rows.append(['<b>Итого</b>',N(sum(FIRSTBUY.values())),'',f"<b>{M(tot+2249)}</b>",f"<b>{M(sum(FIRSTBUY[s]*RET[s] for s in SKUS))}</b>",f"<b>{M(sum(FIRSTBUY[s]*unit(s,first_cost[s])[0] for s in SKUS))}</b>"])
fp_tbl=tbl(['Позиция','Банок','Цена банки','Сумма','Товар по рознице','Прибыль, если всё уйдёт в TikTok'],fp_rows,total_rows=(len(fp_rows)-1,))

def sku_year(Y,label):
    rows=[]
    for s in ORDER:
        u=Y['sku_ch'][s]; ut=sum(u.values())
        rows.append([NAMES[s],N(u['tt']),N(u['sh']),N(u['az']),N(ut),M(Y['sku_rev'][s]),M(Y['sku_prof'][s]),f"{Y['sku_prof'][s]/sum(Y['sku_prof'].values())*100:.0f}%",M(Y['sku_prof'][s]/ut,2)])
    ut=sum(sum(Y['sku_ch'][s].values()) for s in SKUS)
    rows.append(['<b>Всего</b>',N(sum(Y['sku_ch'][s]['tt'] for s in SKUS)),N(sum(Y['sku_ch'][s]['sh'] for s in SKUS)),N(sum(Y['sku_ch'][s]['az'] for s in SKUS)),N(ut),M(sum(Y['sku_rev'].values())),M(sum(Y['sku_prof'].values())),'100%',M(sum(Y['sku_prof'].values())/ut,2)])
    return tbl(['Продукт','Банок TikTok','Банок Shopify','Банок Amazon','Банок всего','Выручка','Прибыль','Доля прибыли','Прибыль с банки'],rows,total_rows=(4,))
sku1=sku_year(Y1,'1'); sku2=sku_year(Y2,'2')

# offers
off_rows=[]
c1k={s:tier_cost(s,1000) for s in SKUS}
for n,p,it,sh,w in FIRST:
    g=sum(c1k[s]*k for s,k in it.items())
    tt=p-g-p*.39-sh-2.5; shp=p-g-(p*.049+.30)-sh-2.5
    off_rows.append([n,M(p,2),M(g,2),M(tt,2),M(shp,2),f"{w*100:.0f}%"])
off_tbl=tbl(['Первая покупка','Цена','Товар','Прибыль TikTok','Прибыль Shopify','Доля заказов'],off_rows)
sub_rows=[]
for n,p,it,sh,w in SUBS:
    g=sum(c1k[s]*k for s,k in it.items()); pr=p-g-(p*.049+.30)-sh-2.5
    sub_rows.append([n,M(p,2),M(g,2),M(pr,2),M(pr*12),f"{w*100:.0f}%"])
sub_tbl=tbl(['Подписка Shopify, в месяц','Цена','Товар','Прибыль в месяц','В год','Доля'],sub_rows)

# quarterly
qv=[];qm=[];qc=[]
for i,q in enumerate(Q):
    qv.append([QN[i],f"{o[i*3]['creators']}-{o[i*3+2]['creators']}",N(q['videos']),N(q['orders']['tt']),N(q['orders']['sh_first']),N(q['orders']['sh_sub']),N(q['orders']['az']),N(q['subs'])])
    qm.append([QN[i].split(' · ')[0],M(q['rev']['tt']),M(q['rev']['sh']),M(q['rev']['az']),M(sum(q['rev'].values())),M(q['goods']),M(q['creator']),M(q['platform']),M(q['ship']),M(q['returns']+q['ppc']+q['fixed']),'<b>'+M(q['profit'])+'</b>'])
    qc.append([QN[i].split(' · ')[0]]+[N(sum(o[j]['units'][s] for j in range(i*3,i*3+3))) for s in ORDER]+[M(q['buy']),M(q['cash']),M(q['lost'])])
def yrow_v(Y,l): return [f"<b>{l}</b>",'',N(Y['videos']),N(Y['orders']['tt']),N(Y['orders']['sh_first']),N(Y['orders']['sh_sub']),N(Y['orders']['az']),N(Y['subs'])]
def yrow_m(Y,l): return [f"<b>{l}</b>",M(Y['rev']['tt']),M(Y['rev']['sh']),M(Y['rev']['az']),M(sum(Y['rev'].values())),M(Y['goods']),M(Y['creator']),M(Y['platform']),M(Y['ship']),M(Y['returns']+Y['ppc']+Y['fixed']),'<b>'+M(Y['profit'])+'</b>']
qv=qv[:4]+[yrow_v(Y1,'Год 1')]+qv[4:]+[yrow_v(Y2,'Год 2')]
qm=qm[:4]+[yrow_m(Y1,'Год 1')]+qm[4:]+[yrow_m(Y2,'Год 2')]
qv_tbl=tbl(['Период','Криейторов','Роликов','Заказов TikTok','Shopify первые','Shopify подписка','Amazon','Подписчиков на конец'],qv,total_rows=(4,9))
qm_tbl=tbl(['Период','TikTok','Shopify','Amazon','Выручка','Товар','Криейторы','Площадки, FBA','Доставка, склад','Возвраты, PPC, пост.','Прибыль'],qm,cls='small',total_rows=(4,9))
qc_tbl=tbl(['Период']+[NAMES[s] for s in ORDER]+['Перезаказы Vox','Касса на конец','Упущено'],qc)

# Q1 monthly
m_rows=[]
for i,lab in enumerate(['20-30 ноября','Декабрь','Январь']):
    r=o[i]; m_rows.append([lab,N(r['orders']['tt']),N(r['orders']['sh_first']),N(r['orders']['sh_sub']),M(sum(r['rev'].values())),M(r['profit']),M(r['buy']),M(r['cash']),M(r['lost'])])
m_tbl=tbl(['Месяц','Заказов TikTok','Shopify первые','Подписка','Выручка','Прибыль','Перезаказ Vox','Касса на конец','Упущено'],m_rows)

# scenario compare
sc_rows=[['Стандарт, Amazon осторожный',K(sum(B1['rev'].values())),K(B1['profit']),K(sum(B2['rev'].values())),K(B2['profit']),'май 2027'],
         ['<b>Стандарт, Amazon стандартный</b>',f"<b>{K(sum(Y1['rev'].values()))}</b>",f"<b>{K(Y1['profit'])}</b>",f"<b>{K(sum(Y2['rev'].values()))}</b>",f"<b>{K(Y2['profit'])}</b>",'<b>май 2027</b>']]
sc_tbl=tbl(['Сценарий','Выручка год 1','Прибыль год 1','Выручка год 2','Прибыль год 2','Темп $1 млн'],sc_rows)
az_cmp=tbl(['Amazon','Осторожный','Стандартный'],[
  ['Старт','март 2027','март 2027'],
  ['Продаж в день на продукт','с 0,8 до 13','с 5 до 30 за полгода, дальше +1,5 в месяц'],
  ['Заказов год 1',N(B1['orders']['az']),N(Y1['orders']['az'])],['Заказов год 2',N(B2['orders']['az']),N(Y2['orders']['az'])],
  ['Реклама PPC, доля цены','20%','15%'],
  ['Выручка Amazon год 1',M(B1['rev']['az']),M(Y1['rev']['az'])],['Выручка Amazon год 2',M(B2['rev']['az']),M(Y2['rev']['az'])]],numcols={1,2})
sens=tbl(['Если не сработает одно допущение','Прибыль год 1','Прибыль год 2','Темп $1 млн'],[
  ['<b>Базовый: стандарт, Amazon стандартный</b>','<b>'+K(1153410)+'</b>','<b>'+K(4104976)+'</b>','<b>май 2027</b>'],
  ['В подписку переходят 20% вместо 15%',K(1329099),K(4893306),'апрель 2027'],
  ['Отток подписки 12% вместо 10%',K(1127692),K(3896765),'май 2027'],
  ['3 500 просмотров на ролик вместо 5 000',K(876953),K(3046397),'июнь 2027'],
  ['Конверсия 0,03% вместо 0,05%',K(781099),K(2689994),'июль 2027'],
  ['Выходит 60% роликов вместо 8 из 8',K(781099),K(2689994),'июль 2027'],
  ['Всё консервативно (расчёт утра 03.10)',K(218620),K(788770),'сентябрь 2028']])

PLAN=[
 ('Решения владельца',[
  ('03.10-06.10','Имя на документах Vox: The Aldera вместо Corvital Plus','владелец'),
  ('03.10-06.10','Вложение: $20 000 или $25 000','владелец'),
 ]),
 ('Поставщик и товар',[
  ('до 06.10','Письмо Tyler Hall: срок от макета до отгрузки, печать этикетки в цене, макеты 4 позиций, капсулы и хранение пробиотика, ранняя отгрузка образцов, объём на год','черновик я, отправка Полина после «отправляй»'),
  ('до 12.10','Макеты 4 этикеток на шаблонах Vox: имя бренда и Distributed by 518 GROUP LLC','дизайнер, задачами'),
  ('до 15.10','Утвердить 4 макета','владелец'),
  ('около 20.10','Оплатить заказ Vox на 518 GROUP LLC','владелец'),
  ('до 05.11','Ранняя отгрузка 90 банок на образцы','Vox'),
 ]),
 ('Юрлицо и площадки',[
  ('до 10.10','Подписать Operating Agreement и Bank Account Resolution, открыть счёт','владелец'),
  ('до 10.10','Купить GS1 и 4 GTIN на 518 GROUP LLC','владелец'),
  ('до 10.10','Подать заявку USPTO на словесный знак THE ALDERA, класс 5. Номер заявки нужен для Amazon Brand Registry','владелец, черновик я'),
  ('до 15.10','Регистрация TikTok Shop Seller, Shopify с Shopify Payments, Amazon Seller Central Professional','владелец'),
  ('до 15.10','Выбрать склад-отправщик во Флориде, договор до старта','подбор я, решение владелец'),
 ]),
 ('Криейторы',[
  ('до 15.10','Отобрать 100 кандидатов, подписать 50: 8 роликов в месяц за 30%','Полина'),
  ('до 10.11','Образцы у всех 50, бриф: Flip the jar, утренняя рутина, «я убрала лишнее»','Полина'),
  ('с 20.11 еженедельно','Учёт вышедших роликов, замена тех, кто не выпускает','Полина'),
  ('с декабря','Плюс 10 криейторов в месяц до 150, дальше плюс 12','Полина'),
 ]),
 ('Магазин Shopify',[
  ('до 31.10','Магазин, подписка на Foundation, Gut Duo, Daily Four, бандлы','я'),
  ('до 31.10','Письма: день 0, день 7, день 25 с предложением подписки. Вкладыш с кодом в каждой посылке','я'),
 ]),
 ('Запуск',[
  ('20.11','Старт продаж TikTok Shop и Shopify','все'),
  ('27.11 и 30.11','Black Friday и Cyber Monday','все'),
  ('декабрь','Перезаказ Vox дважды в месяц, 1-го и 15-го: в декабре товара впритык','я расчёт, владелец оплата'),
 ]),
 ('Amazon',[
  ('январь 2027','COA партии из лаборатории ISO 17025 для допуска к категории добавок, Brand Registry','я, владелец'),
  ('февраль 2027','Листинги, A+ контент «What’s inside», первая поставка FBA, Vine','я'),
  ('март 2027','Старт Amazon, PPC. Цель: 30 продаж в день на продукт к сентябрю','я'),
 ]),
 ('Рост',[
  ('апрель 2027','Менеджер криейторов и поддержка клиентов: больше 90 заказов в день','владелец'),
  ('май 2027','Подтвердить у Vox объём на год: около 5 000 банок колострума в месяц к осени','я'),
  ('июнь 2027','Квалифицировать SMP как второй источник','я'),
  ('август 2027','Переход на ступень 5 000 по всем позициям, подготовка к Black Friday 2027','я, владелец'),
 ]),
]
plan_html=''
for g,items in PLAN:
    plan_html+=f'<h3>{g}</h3>'+tbl(['Срок','Действие','Кто'],[[a,b,c] for a,b,c in items],numcols=set())

chart_vals=[r['profit'] for r in o]
mx=max(chart_vals)*1.08
W,H,L,R,T,B=700,230,64,10,12,34; pw=W-L-R; ph=H-T-B; bw=pw/24
def yy(v): return T+ph-(v/mx)*ph
svg=f'<svg viewBox="0 0 {W} {H}" width="100%">'
step=100000
for v in range(0,int(mx)+1,step):
    svg+=f'<line x1="{L}" x2="{W-R}" y1="{yy(v):.1f}" y2="{yy(v):.1f}" stroke="#D6DDD8"/><text x="{L-6}" y="{yy(v)+3:.1f}" text-anchor="end" class="ax">${v//1000}k</text>'
for i,v in enumerate(chart_vals):
    col='#A4512A' if v*12>=1e6 else '#2C6A55'
    svg+=f'<rect x="{L+i*bw+bw*.18:.1f}" y="{yy(v):.1f}" width="{bw*.64:.1f}" height="{T+ph-yy(v):.1f}" fill="{col}"/>'
g=1e6/12
svg+=f'<line x1="{L}" x2="{W-R}" y1="{yy(g):.1f}" y2="{yy(g):.1f}" stroke="#A4512A" stroke-dasharray="5 4"/><text x="{L+6}" y="{yy(g)-5:.1f}" class="ax" fill="#A4512A">$1 млн в год</text>'
for k,l in {1:'ноя 26',7:'май 27',12:'окт 27',18:'апр 28',24:'окт 28'}.items():
    x=L+(k-1)*bw+bw/2; svg+=f'<text x="{x:.1f}" y="{H-18}" text-anchor="middle" class="ax">М{k}</text><text x="{x:.1f}" y="{H-5}" text-anchor="middle" class="ax">{l}</text>'
svg+='</svg>'

ch1={k:Y1['rev'][k]/sum(Y1['rev'].values())*100 for k in Y1['rev']}; ch2={k:Y2['rev'][k]/sum(Y2['rev'].values())*100 for k in Y2['rev']}

APLUS='A+ контент «What’s inside»: панель крупно, одна цифра, сравнение с бленд-формулами без названия конкурентов'
CSS='''
@page{size:A4;margin:14mm 13mm 15mm 13mm}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"DejaVu Sans",sans-serif;font-size:8.6pt;line-height:1.42;color:#18211E;margin:0}
h1{font-family:"DejaVu Serif",serif;font-size:21pt;line-height:1.15;margin:0 0 6pt;color:#18211E}
h2{font-family:"DejaVu Serif",serif;font-size:13pt;margin:14pt 0 6pt;color:#2C6A55;border-bottom:.8pt solid #2C6A55;padding-bottom:3pt;page-break-after:avoid}
h3{font-size:9.6pt;margin:9pt 0 4pt;page-break-after:avoid}
p{margin:0 0 5pt}
.kicker{font-size:7.4pt;letter-spacing:.14em;text-transform:uppercase;color:#5A6762;font-weight:bold}
.lede{font-size:10pt;color:#3d4844;margin-bottom:8pt}
table{width:100%;border-collapse:collapse;margin:3pt 0 7pt;font-size:7.9pt;page-break-inside:avoid}
table.small{font-size:7.1pt}
th{background:#E2EEE8;color:#18211E;text-align:left;font-weight:bold;padding:3.5pt 4pt;border-bottom:.8pt solid #2C6A55;vertical-align:bottom}
td{padding:3.2pt 4pt;border-bottom:.5pt solid #D6DDD8;vertical-align:top}
td.n,th.n{text-align:right;white-space:nowrap;font-family:"DejaVu Sans Mono",monospace}
tr.total td{font-weight:bold;background:#F1F5F2}
.mut{color:#6b7772;font-size:7pt}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:.8pt solid #D6DDD8;margin:6pt 0 8pt}
.kpi{padding:7pt 8pt;border-right:.6pt solid #D6DDD8;border-bottom:.6pt solid #D6DDD8}
.kpi b{display:block;font-family:"DejaVu Sans Mono",monospace;font-size:14pt;color:#2C6A55}
.kpi span{font-size:7.6pt;color:#5A6762}
.callout{border-left:2.4pt solid #A4512A;background:#F6E7DE;padding:6pt 8pt;margin:5pt 0 8pt}
.jars{display:grid;grid-template-columns:repeat(4,1fr);gap:6pt;margin:6pt 0}
.jar{border:.8pt solid #D6DDD8;padding:8pt}
.jar .b{font-size:6.6pt;letter-spacing:.2em;color:#5A6762;font-weight:bold}
.jar .r{font-family:"DejaVu Sans Mono",monospace;font-size:7pt;letter-spacing:.12em;color:#2C6A55}
.jar .nm{font-family:"DejaVu Serif",serif;font-size:10.5pt;font-weight:bold;margin:2pt 0}
.jar .big{font-family:"DejaVu Sans Mono",monospace;font-size:8.6pt;border-top:.6pt solid #D6DDD8;padding-top:4pt;margin-top:4pt}
.jar .pr{font-size:7pt;color:#5A6762}
.promise{font-family:"DejaVu Serif",serif;font-size:15pt;margin:4pt 0 6pt}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12pt}
ul{margin:0 0 5pt;padding-left:13pt}li{margin-bottom:2pt}
.pb{page-break-before:always}
.ax{font-family:"DejaVu Sans Mono",monospace;font-size:8px;fill:#5A6762}
.foot{font-size:7pt;color:#6b7772;border-top:.5pt solid #D6DDD8;padding-top:5pt;margin-top:10pt}
'''
doc=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>The Aldera: анализ, товары и план</title><style>{CSS}</style></head><body>
<div class="kicker">The Aldera · 518 GROUP LLC · 03.10.2026 · стандартный расчёт</div>
<h1>Четыре продукта, экономика по товарам, позиционирование и план действий</h1>
<p class="lede">Вложение $20 000. Старт продаж 20.11.2026. 50 криейторов, 30% комиссии за 8 роликов в месяц. Три канала: TikTok Shop, Shopify, Amazon. Все четыре продукта у Vox Nutrition в наличии, этикетка копирует макет завода. Прибыль до рекламного бюджета, зарплат и налогов.</p>

<div class="kpis">
<div class="kpi"><b>{M(19750)}</b><span>первая закупка и запуск</span></div>
<div class="kpi"><b>декабрь 2026</b><span>прибыль перекрывает вложение</span></div>
<div class="kpi"><b>{MON[hit-1]}</b><span>темп $1 млн прибыли в год</span></div>
<div class="kpi"><b>{K(Y1['profit'])}</b><span>прибыль года 1, выручка {K(sum(Y1['rev'].values()))}</span></div>
<div class="kpi"><b>{K(Y2['profit'])}</b><span>прибыль года 2, выручка {K(sum(Y2['rev'].values()))}</span></div>
<div class="kpi"><b>{N(Y2['subs'])}</b><span>подписчиков через 24 месяца</span></div>
</div>
<p>Год 1 это 20.11.2026-31.10.2027, год 2 это ноябрь 2027-октябрь 2028. Основной сценарий в документе: стандартные допущения по TikTok и Shopify плюс стандартный Amazon.</p>
<div class="callout"><b>Узкое место не спрос, а деньги на товар в декабре.</b> При $20 000 в декабре склада хватает примерно на 87% спроса, теряется {M(o[1]['lost'])} выручки в пиковый месяц: половина выплат TikTok приходит только в следующем месяце. При вложении $25 000 нехватки нет, прибыль года 1 выше на {M(1174706-1153410)}. Без доплаты: перезаказ Vox дважды в месяц или отсрочка платежа у Vox.</div>

<h2>1. Допущения</h2>
{tbl(['Параметр','В расчёте'],[
['Роликов с криейтора','8 в месяц, все выходят'],['Просмотров на ролик','5 000'],['Конверсия просмотра в заказ','0,05%'],['Органика и поиск сверху','+20%'],
['Прямые заказы на Shopify','10% от заказов TikTok'],['Переходят в подписку','15% первых покупателей'],['Отток подписки','10% в месяц'],
['Криейторов','50 в ноябре и декабре, плюс 10 в месяц до 150, дальше плюс 12'],['Сезон','ноябрь и декабрь +15%, январь +10%'],
['Amazon, стандартный','с марта 2027: 5 продаж в день на продукт, за полгода до 30, дальше +1,5 в месяц; реклама 15% цены'],
['Комиссии','TikTok 6%, криейтор 30%, Shopify 2,9% + $0.30, Amazon 15% + FBA'],
['Доставка и склад','$3.50-5.50 за банку по весу, $2.50 за заказ склад-отправщик'],['Возвраты','TikTok 3%, Shopify 2%'],
['Постоянные расходы','$500 в месяц в год 1, $1 000 в год 2'],
['Товар','цены Vox 2026 Q3 по ступени объёма каждого перезаказа']],numcols=set())}

<h2 class="pb">2. Позиционирование бренда</h2>
<div class="jars">
<div class="jar"><div class="b">THE ALDERA</div><div class="r">GUT</div><div class="nm">Colostrum</div><div class="big">2,000 mg · 400 mg IgG</div><div class="pr">$39.95 · 30 порций</div></div>
<div class="jar"><div class="b">THE ALDERA</div><div class="r">BALANCE</div><div class="nm">Women's Probiotic</div><div class="big">50 Billion CFU</div><div class="pr">$34.95 · 60 капсул</div></div>
<div class="jar"><div class="b">THE ALDERA</div><div class="r">REST</div><div class="nm">Magnesium Glycinate</div><div class="big">100% glycinate</div><div class="pr">$29.95 · 90 капсул</div></div>
<div class="jar"><div class="b">THE ALDERA</div><div class="r">STRENGTH</div><div class="nm">Creatine</div><div class="big">5 g monohydrate</div><div class="pr">$29.95 · 60 порций</div></div>
</div>
<div class="promise">Four basics. Nothing to decode.</div>
<p>Четыре базовых продукта, нечего расшифровывать. Стоит под мастер-теглайном платформы бренда от 10.09: <b>What you see is what you get.</b> Платформа не меняется, здесь она переложена на линейку и покупателя.</p>
<div class="two"><div>
<h3>Для кого</h3><p>Женщина 25-45, покупает добавки в TikTok Shop и на Amazon. Устала от банок с 20 ингредиентами и обещаниями, которые нечем проверить. Хочет базовые вещи, понятные с первого взгляда. Упаковка нейтральная, креатин и магний берут и мужчины, но голос бренда и криейторы женские.</p>
<h3>Почему это цепляет</h3><p>Рынок добавок в TikTok продаёт обещанием «моя жизнь изменилась», и покупательница перестала ему верить. The Aldera продаёт цифрой: одно число крупно на лицевой стороне и то же число на обороте. Спокойная уверенность вместо хайпа.</p>
</div><div>
<h3>Банка</h3><ul><li>Сверху THE ALDERA</li><li>Роль одним словом: GUT, BALANCE, REST, STRENGTH</li><li>Название продукта</li><li><b>Одна цифра крупно</b></li><li>Оборот: панель с макета Vox, Distributed by 518 GROUP LLC</li></ul>
<h3>Ритуал дня</h3><ul><li><b>Утро:</b> Colostrum, Women's Probiotic, Creatine</li><li><b>Вечер:</b> Magnesium Glycinate</li></ul>
</div></div>
<h3>Роль каждого канала в позиционировании</h3>
{tbl(['Канал','Задача','Чем говорит бренд'],[
['TikTok Shop','приводит нового покупателя','Flip the jar: 15 секунд, цифра спереди, переворот, та же цифра на обороте. Утренняя рутина. «Я убрала лишнее»: было девять банок, стало четыре'],
['Shopify','удерживает: подписка и наборы','система из четырёх банок, наборы Foundation, Gut Duo, Daily Four, вкладыш с кодом подписки'],
['Amazon','ловит поиск и отзывы',APLUS]],numcols=set())}
<h3>Цена в рынке</h3>
{tbl(['Сегмент','Цена банки','Что продаёт'],[['Массовый Amazon','$15-25','цену за количество'],['<b>The Aldera</b>','<b>$30-40</b>','<b>проверяемую цифру и понятный состав</b>'],['Премиальный DTC','$50-100+','историю бренда и обещание']],numcols={1})}
<h3>Почему именно эти четыре</h3>
{tbl(['Продукт','Спрос','Риск'],[
['Colostrum','одна из самых быстрорастущих категорий TikTok Shop','спецификация подписана, Prop 65 на макете нет'],
["Women's Probiotic",'женское здоровье это крупнейший сегмент покупателей добавок в TikTok Shop','живые культуры, нет типичной проблемы со свинцом'],
['Magnesium Glycinate','одна из главных категорий Amazon, тренд «магний для сна»','чистый глицинат, без оксида'],
['Creatine','вторая волна: креатин для женщин и для мозга','креатинин в сырье не выше 100 ppm']],numcols=set())}
<p class="mut">Отклонены: электролит и ашваганда (Prop 65 на макете), Magnesium Complex (40% магния из оксида), Greens и Sea Moss (риск тяжёлых металлов), Omega 3 и Collagen (после комиссий прибыли почти не остаётся), GLP1 и Berberine (категория держится на заявлениях о болезни).</p>

<h2 class="pb">3. Разбивка по товарам</h2>
<h3>Первая закупка на $20 000</h3>
{fp_tbl}
<p class="mut">Пробиотик 400 и креатин 250 идут по ступеням 300 и 150, поэтому дороже за банку. С первым перезаказом цена падает до ступени 1 000 и ниже.</p>
<h3>Цена, себестоимость и прибыль с одной банки по каналам</h3>
{unit_tbl}
<p class="mut">Прибыль после товара, комиссий, криейтора 30% (только TikTok), доставки, склада и возвратов. Amazon после комиссии 15%, FBA и рекламы 15% цены. Процент это доля прибыли в розничной цене.</p>
<h3>Наборы и подписка</h3>
{off_tbl}
{sub_tbl}
<p>Подписчик приносит почти втрое больше первой покупки в TikTok, причём каждый месяц. Поэтому TikTok работает на привлечение, а прибыль зарабатывает подписка на Shopify.</p>
<h3>Год 1 по товарам</h3>
{sku1}
<h3>Год 2 по товарам</h3>
{sku2}
<p class="mut">Наборы разнесены по товарам пропорционально розничной цене. Прибыль до постоянных расходов ($6 000 в год 1, $12 000 в год 2).</p>

<h2 class="pb">4. Прогноз по 3 месяца</h2>
<h3>Прибыль по месяцам</h3>
{svg}
<h3>Объём</h3>
{qv_tbl}
<h3>Выручка, расходы, прибыль</h3>
{qm_tbl}
<p>Доли выручки: год 1 TikTok {ch1['tt']:.0f}%, Shopify {ch1['sh']:.0f}%, Amazon {ch1['az']:.0f}%. Год 2 TikTok {ch2['tt']:.0f}%, Shopify {ch2['sh']:.0f}%, Amazon {ch2['az']:.0f}%.</p>
<h3>Товар (банок) и касса</h3>
{qc_tbl}
<p class="mut">Касса накопительная, до рекламного бюджета, зарплат, налогов и вывода денег. Перезаказы оплачиваются из выручки с запасом на 1,3 месяца продаж.</p>

<h3>Первый квартал по месяцам: как работают $20 000</h3>
{m_tbl}
<ul><li>В ноябре на перезаказ свободно только {M(o[0]['buy'])}: половина выплат TikTok приходит в следующем месяце.</li>
<li>В декабре склада хватает примерно на 87% спроса. С января касса растёт сама, нехватки больше нет.</li></ul>

<h2 class="pb">5. Сценарии</h2>
<h3>Amazon осторожный против стандартного</h3>
{az_cmp}
{sc_tbl}
<h3>Чувствительность основного сценария</h3>
{sens}
<p>Самые сильные рычаги: доля перехода в подписку, просмотры на ролик и выход всех 8 роликов. Все три зависят от отбора криейторов и работы магазина, а не от денег.</p>
<h3>Что не входит в расчёт</h3>
{tbl(['Статья','Когда появится'],[['Рекламный бюджет TikTok и Meta','по решению владельца, считается отдельно'],['Менеджер криейторов, поддержка клиентов','с весны 2027, больше 90 заказов в день'],['Налоги','по итогам года'],['Страховка ответственности под объём','Amazon требует при продажах от $10 тыс. в месяц']],numcols=set())}

<h2>6. План действий со сроками</h2>
{plan_html}

<h2>7. Риски</h2>
{tbl(['Риск','Последствие','Чем снимается'],[
['Нехватка товара в декабре','теряется около $23 тыс. выручки','вложение $25 000 или перезаказ дважды в месяц'],
['Мощность Vox','к осени 2027 около 5 000 банок колострума в месяц','подтвердить годовой объём в мае, SMP вторым источником'],
['Выплаты TikTok новому продавцу','новым магазинам TikTok может дольше удерживать выплаты','уточнить при регистрации 518 GROUP LLC'],
['Криейторы не выпускают 8 роликов','при 60% прибыль года 1 около $781 тыс.','учёт роликов еженедельно, замена неактивных'],
['Срок Vox от макета до отгрузки','больше 20 рабочих дней сдвигает старт 20.11','ответ Tyler Hall, макеты утвердить до 15.10'],
['Пробиотик на 60 дней или требует холода','меняется цена и доставка','макет и условия хранения от Vox'],
['Amazon не даёт допуск к добавкам','канал стартует позже марта','COA из лаборатории ISO 17025 заранее, в январе']],numcols=set())}

<div class="foot">Модель помесячная на 24 месяца с 20.11.2026, с учётом склада и кассы: продажа не больше остатка, выплаты TikTok и Amazon наполовину в следующем месяце, перезаказ Vox оплачивается сразу и приходит к следующему месяцу. Скрипт: tools/model_daily_four_std.py и tools/model_daily_four_amz.py в репозитории.</div>
</body></html>'''
open('aldera_analysis.html','w').write(doc)
print('ok',hit, round(Y1['profit']),round(Y2['profit']))
