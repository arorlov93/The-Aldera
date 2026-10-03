"""Generate The Aldera business plan (HTML -> PDF via headless Chromium). Numbers from twin.py (verified = Excel)."""
import json, subprocess
from twin import *
A=json.load(open('analysis.json'))
import math
T2=int(math.ceil((A['mc']['need_p90']+5000)/1000.0)*1000)
MN=['','ноябрь 2026','декабрь 2026','январь 2027','февраль 2027','март 2027','апрель 2027','май 2027','июнь 2027','июль 2027','август 2027','сентябрь 2027','октябрь 2027']
TTV=FIX['tt_fee']+FIX['cr_pct']+FIX['tt_ret']
def offer_profit(price,ship,q,ch):
    c=sum(PROD[s]['p'][3]*q[i] for i,s in enumerate(SK))
    return price-c-(price*TTV if ch=='tt' else price*.049+.30)-ship-2.5
FP_TT=sum(offer_profit(o[0],o[1],o[3],'tt')*o[2] for o in OFF); SUB_P=sum(offer_profit(o[0],o[1],o[3],'sh')*o[2] for o in SUBS)
VIEWS=SCEN['v1'][1]
CR_ORD=8*VIEWS*0.0005*1.2
o=run(params(2)); B=summary(o)
C1='#00856A'; C2='#D08A2E'; INK='#18211E'; MUT='#5A6762'; LINE='#D6DDD8'; ACC='#2C6A55'
def fm(v): return f"{v:,.0f}".replace(',',' ')
def M(v): return ('−$' if v<0 else '$')+fm(abs(v))
def K(v): return (f"${v/1e6:.2f} млн".replace('.',',') if abs(v)>=1e6 else f"${v/1e3:.0f} тыс.")
def P(v,d=0): return (f"{v*100:.{d}f}%").replace('.',',')
def tbl(head,rows,num=None,total=()):
    num=set(range(1,len(head))) if num is None else num
    h='<table><thead><tr>'+''.join(f'<th class="{"n" if i in num else ""}">{x}</th>' for i,x in enumerate(head))+'</tr></thead><tbody>'
    for ri,r in enumerate(rows):
        h+=f'<tr class="{"total" if ri in total else ""}">'+''.join(f'<td class="{"n" if i in num else ""}">{x}</td>' for i,x in enumerate(r))+'</tr>'
    return h+'</tbody></table>'
MON=['окт 26','ноя 26','дек 26','янв 27','фев 27','мар 27','апр 27','май 27','июн 27','июл 27','авг 27','сен 27','окт 27']
def yv(k,y): return year(o,y,k)

def axl(v): return '$0' if v==0 else '$'+(f'{v/1e6:.1f}').replace('.',',')+' млн'
# ---- chart 1: monthly revenue & EBITDA (36 months), one $ axis ----
def chart_monthly():
    W,H,L,R,T,Bm=720,250,62,90,14,34; pw=W-L-R; ph=H-T-Bm
    rev=[r['rev'] for r in o[1:]]; eb=[r['ebitda'] for r in o[1:]]; n=len(rev); mx=1.6e6
    y=lambda v: T+ph-(v/mx)*ph; bw=pw/n
    s=f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Выручка и EBITDA по месяцам">'
    for v in range(0,int(mx)+1,400000):
        s+=f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{LINE}" stroke-width="0.6"/><text x="{L-6}" y="{y(v)+3:.1f}" text-anchor="end" class="ax">{axl(v)}</text>'
    for i,(a,b) in enumerate(zip(rev,eb)):
        x=L+i*bw; w=bw*0.42
        s+=f'<rect x="{x+bw*0.06:.1f}" y="{y(a):.1f}" width="{w:.1f}" height="{T+ph-y(a):.1f}" fill="{C1}" rx="1"/>'
        s+=f'<rect x="{x+bw*0.06+w+1:.1f}" y="{y(b):.1f}" width="{w:.1f}" height="{T+ph-y(b):.1f}" fill="{C2}" rx="1"/>'
    s+=f'<text x="{L+(n-1)*bw+bw/2+14:.1f}" y="{y(rev[-1])+4:.1f}" class="lab">{K(rev[-1])}</text><text x="{L+(n-1)*bw+bw/2+14:.1f}" y="{y(eb[-1])+4:.1f}" class="lab">{K(eb[-1])}</text>'
    for k,l in {1:'ноя 26',7:'май 27',13:'ноя 27',19:'май 28',25:'ноя 28',31:'май 29',36:'окт 29'}.items():
        x=L+(k-1)*bw+bw/2; s+=f'<text x="{x:.1f}" y="{H-16}" text-anchor="middle" class="ax">{l}</text>'
    s+=f'<rect x="{L}" y="{H-10}" width="9" height="9" fill="{C1}"/><text x="{L+13}" y="{H-2}" class="ax">Выручка в месяц</text><rect x="{L+120}" y="{H-10}" width="9" height="9" fill="{C2}"/><text x="{L+133}" y="{H-2}" class="ax">EBITDA в месяц</text>'
    return s+'</svg>'
# ---- chart 2: Monte Carlo histogram Y2 EBITDA ----
def chart_hist():
    hs=A['mc']['hist_y2']; W,H,L,R,T,Bm=720,190,44,10,16,36; pw=W-L-R; ph=H-T-Bm; mx=0.45
    y=lambda v: T+ph-(v/mx)*ph; bw=pw/len(hs)
    s=f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Распределение EBITDA года 2">'
    for v in (0,.1,.2,.3,.4): s+=f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{LINE}" stroke-width="0.6"/><text x="{L-6}" y="{y(v)+3:.1f}" text-anchor="end" class="ax">{int(v*100)}%</text>'
    for i,(lab,v) in enumerate(hs):
        x=L+i*bw+bw*.12; w=bw*.76
        if v>0: s+=f'<rect x="{x:.1f}" y="{y(v):.1f}" width="{w:.1f}" height="{T+ph-y(v):.1f}" fill="{C1}" rx="2"/>'
        s+=f'<text x="{x+w/2:.1f}" y="{y(v)-4:.1f}" text-anchor="middle" class="lab">{P(v,1) if v else ""}</text><text x="{x+w/2:.1f}" y="{H-20}" text-anchor="middle" class="ax">{lab}</text>'
    s+=f'<text x="{L}" y="{H-4}" class="ax">EBITDA года 2, доля из {fm(A["mc_n"])} прогонов</text>'
    return s+'</svg>'
# ---- chart 3: tornado Y2 EBITDA ----
def chart_tornado():
    t=A['tornado'][:9]; base=B['ebitda2']; W,L,R=720,250,20; rowh=22; H=len(t)*rowh+40
    lo=min(min(a[3],a[4]) for a in t); hi=max(max(a[3],a[4]) for a in t); lo=min(lo,base)*0.95; hi=hi*1.03
    x=lambda v: L+(v-lo)/(hi-lo)*(W-L-R)
    s=f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Торнадо по EBITDA года 2">'
    for i,a in enumerate(t):
        yy=10+i*rowh; bad=min(a[3],a[4]); good=max(a[3],a[4])
        s+=f'<text x="{L-8}" y="{yy+12}" text-anchor="end" class="ax">{a[0]}</text>'
        s+=f'<rect x="{x(bad):.1f}" y="{yy+3}" width="{x(base)-x(bad):.1f}" height="13" fill="{C2}" rx="2"/>'
        s+=f'<rect x="{x(base):.1f}" y="{yy+3}" width="{x(good)-x(base):.1f}" height="13" fill="{C1}" rx="2"/>'
    s+=f'<line x1="{x(base):.1f}" x2="{x(base):.1f}" y1="6" y2="{H-26}" stroke="{INK}" stroke-width="1"/><text x="{x(base):.1f}" y="{H-14}" text-anchor="middle" class="ax">база {K(base)}</text>'
    s+=f'<rect x="{L}" y="{H-10}" width="9" height="9" fill="{C2}"/><text x="{L+13}" y="{H-2}" class="ax">плохое значение</text><rect x="{L+120}" y="{H-10}" width="9" height="9" fill="{C1}"/><text x="{L+133}" y="{H-2}" class="ax">хорошее значение</text>'
    return s+'</svg>'

# tables
y3=[(f'Год {y}',) for y in (1,2,3)]
pl_rows=[]
PL=[('Выручка TikTok Shop','r_tt'),('Выручка Shopify: первые','r_sf'),('Выручка Shopify: подписка','r_ss'),('Выручка Amazon','r_az'),('<b>Выручка всего</b>','rev'),
    ('Товар (Vox)','cogs'),('Комиссии площадок, FBA, эквайринг',None),('Комиссия криейторов','crc'),('Доставка и склад',None),('Возвраты и реклама Amazon',None),
    ('<b>Маржинальная прибыль</b>','contrib'),('Команда','team'),('Сервисы, страховка, бухгалтерия',None),('<b>EBITDA</b>','ebitda'),('Налог, оценка 25%','tax'),('<b>Чистая прибыль</b>','net')]
def g(k,y):
    if k=='plat': return yv('ttfee',y)+yv('shfee',y)+yv('azfee',y)
    if k=='shipx': return yv('ship',y)+yv('fulf',y)
    if k=='retx': return yv('ret',y)+yv('ppc',y)
    if k=='fixo': return yv('soft',y)+yv('ins',y)+yv('acct',y)
    return yv(k,y)
alias={'Комиссии площадок, FBA, эквайринг':'plat','Доставка и склад':'shipx','Возвраты и реклама Amazon':'retx','Сервисы, страховка, бухгалтерия':'fixo'}
tot_idx=[]
for i,(lab,k) in enumerate(PL):
    kk=k or alias[lab]; vals=[g(kk,y) for y in (1,2,3)]
    neg=kk in('cogs','plat','crc','shipx','retx','team','fixo','tax')
    pl_rows.append([lab]+[M(-v) if neg else M(v) for v in vals])
    if lab.startswith('<b>'): tot_idx.append(i)
pl_tbl=tbl(['$','Год 1','Год 2','Год 3'],pl_rows,total=tuple(tot_idx))
q_rows=[]
for q in range(4):
    rs=o[1+3*q:4+3*q]
    q_rows.append([['Q1 ноя-янв','Q2 фев-апр','Q3 май-июл','Q4 авг-окт'][q],fm(rs[-1]['cr']),fm(sum(r['tt'] for r in rs)),fm(sum(r['subord'] for r in rs)),fm(sum(r['az'] for r in rs)),fm(rs[-1]['subs']),M(sum(r['rev'] for r in rs)),M(sum(r['ebitda'] for r in rs)),M(sum(r['buy'] for r in rs)),M(rs[-1]['cash'])])
q_tbl=tbl(['Квартал года 1','Криейторов','Заказы TikTok','Заказы подписки','Заказы Amazon','Подписчиков','Выручка','EBITDA','Закупка Vox','Деньги на конец'],q_rows)
sc=[A['scen_cons'],A['scen_base'],A['scen_opt']]
sc_tbl=tbl(['','Консервативный','Базовый','Оптимистичный'],[
 ['Выручка год 1']+[K(s['rev1']) for s in sc],['EBITDA год 1']+[K(s['ebitda1']) for s in sc],['Выручка год 2']+[K(s['rev2']) for s in sc],['EBITDA год 2']+[K(s['ebitda2']) for s in sc],
 ['EBITDA год 3']+[K(s['ebitda3']) for s in sc],['Подписчиков через 24 мес.']+[fm(s['subs2']) for s in sc],['Темп $1 млн EBITDA в год']+[(f"{s['m1m']}-й месяц" if s['m1m'] else 'не за 36 мес.') for s in sc]],total=())
mc=A['mc']
mc_tbl=tbl(['','P10, плохой из десяти','P50, медиана','P90, хороший из десяти'],[[lab]+[K(mc[k][p]) for p in ('p10','p50','p90')] for lab,k in (('Выручка год 1','rev1'),('EBITDA год 1','ebitda1'),('Выручка год 2','rev2'),('EBITDA год 2','ebitda2'),('EBITDA год 3','ebitda3'))])
st_tbl=tbl(['Событие','EBITDA год 1','EBITDA год 2','Темп $1 млн'],[[s['lab'],K(s['e1']),K(s['e2']),(f"{s['m1m']}-й мес." if s['m1m'] else 'нет')] for s in A['stress']],total=(0,))
fund_tbl=tbl(['Вариант','Минимум денег на счёте','Когда'],[[l,M(v),('октябрь 2026' if m==0 else 'декабрь 2026')] for l,v,m,e in A['funding']])
unit_rows=[]
for s,n in (('COL','Colostrum'),('PRO',"Women's Probiotic"),('MG','Magnesium Glycinate'),('CRE','Creatine')):
    p=PROD[s]; c=p['p'][3]; tt=p['ret']-c-p['ret']*TTV-p['sh']-2.5; sh=p['ret']-c-p['ret']*.049-.3-p['sh']-2.5; az=p['ret']-c-p['ret']*.30-p['fba']
    unit_rows.append([n,M(p['ret'])[:-0]+'' if False else f"${p['ret']:.2f}",f"${c:.2f}",f"${p['p'][5]:.2f}",f"${tt:.2f} · {P(tt/p['ret'])}",f"${sh:.2f} · {P(sh/p['ret'])}",f"${az:.2f} · {P(az/p['ret'])}"])
unit_tbl=tbl(['Продукт','Розница','Банка @1 000','Банка @5 000','Прибыль TikTok','Прибыль Shopify','Прибыль Amazon'],unit_rows)
st={x['lab']:x for x in A['stress']}; tr={t[0]:t for t in A['tornado']}; b1=B['ebitda1']
def dm(v): return '−'+K(v)
risk_rows=[['Криейторы не выпускают 8 роликов','50%',dm(b1-tr['Доля вышедших роликов'][5]),'учёт роликов еженедельно, замена неактивных, бонус лучшим'],
 ['Конверсия ниже базы (0,03%)','30%',dm(b1-tr['Конверсия просмотра в заказ'][5]),'тест хуков, формат Flip the jar, стартовая скидка'],
 ['Подписка слабее плана','25%',dm(b1-st['Подписка не работает: переход 5%, отток 15%']['e1']),'письма на 0, 7 и 25-й день, скидка на первую подписку, вкладыш'],
 ['Криейторов не прибавляется','20%',dm(b1-st['Криейторов не прибавляется: 50 весь срок']['e1']),'аутрич 100 кандидатов в неделю, менеджер криейторов с 5-го месяца'],
 ['Amazon не даёт допуск к добавкам','20%',dm(b1-st['Amazon не дал допуск к категории']['e1']),'COA из лаборатории ISO 17025 в январе, заявка USPTO для Brand Registry'],
 ['TikTok Shop блокирует магазин на 2 месяца','10%',dm(b1-st['TikTok Shop заблокирован на 2 месяца (март-апрель 2027)']['e1']),'этикетка завода дословно, без заявлений о болезни, опора на Shopify и Amazon'],
 ['Spark Ads не окупаются (ROAS 1,5)','20%',dm(b1-st['Spark Ads не окупаются: ROAS 1,5']['e1']),'выключать ролик при ROAS ниже 2 семь дней подряд'],
 ['Цены Vox +15%','15%',dm(b1-st['Цены Vox +15%']['e1']),'годовой объём под цену, SMP вторым источником'],
 ['Vox срывает отгрузку на месяц','15%',dm(b1-st['Vox не отгрузил товар: месяц без продаж (февраль 2027)']['e1']),'запас 1,3 месяца, подтверждение мощности в мае 2027'],
 ['Денег на товар не хватает в декабре',P(mc['p_cash_neg']),'до −$23 тыс. выручки',f'второй транш ${fm(T2)} вместо $5 000']]
risk_tbl=tbl(['Риск','Вероятность','Ущерб, EBITDA год 1','Что делаем'],risk_rows,num={1,2})
team_tbl=tbl(['Роль','В месяц','С какого месяца'],[['Владелец: стратегия, поставщики, деньги','не заложено','сейчас'],['Полина: переписка, криейторы','в текущих расходах','сейчас'],['Менеджер криейторов 1','$4 000','март 2027'],['Поддержка клиентов','$3 000','апрель 2027'],['Менеджер Amazon и операций','$5 000','август 2027'],['Менеджер криейторов 2','$4 000','ноябрь 2027'],['Поддержка клиентов 2','$3 000','февраль 2028'],['Финансы на аутсорсе','$2 000','апрель 2028']],num={1})
plan=[('до 06.10','Письмо Tyler Hall (Vox): срок от макета до отгрузки, печать этикетки в цене, макеты 4 позиций, пробиотик, ранняя отгрузка образцов, срок перезаказа','черновик Claude, отправка Полина после «отправляй»'),
('до 10.10','Operating Agreement и Bank Account Resolution, счёт 518 GROUP LLC; GS1 и 4 GTIN; заявка USPTO THE ALDERA, класс 5','владелец'),
('до 15.10','TikTok Shop Seller, Shopify с Payments, Amazon Seller Central; склад-отправщик во Флориде; 50 криейторов по договору 8 роликов за 30%','владелец, Полина'),
('до 15.10','Макеты 4 этикеток на шаблонах Vox: имя The Aldera и Distributed by 518 GROUP LLC; утверждение','дизайнер, владелец'),
('~20.10','Партия 1 у Vox: $19 755 из транша $20 000','владелец'),
('до 31.10','Shopify: подписка Foundation, Gut Duo, Daily Four; письма 0, 7, 25-й день; вкладыш с кодом','Claude'),
('до 10.11','Образцы у 50 криейторов','Vox, Полина'),
('20.11','Старт продаж TikTok Shop и Shopify; Black Friday 27.11, Cyber Monday 30.11','все'),
('до 25.11',f'Транш 2 (рекомендация ${fm(T2)}) и партия 2 к декабрю','владелец'),
('февраль 2027','Spark Ads на выстрелившие ролики по правилам раздела 5','Полина, Claude'),
('январь 2027','COA партии из ISO 17025 для допуска Amazon; Brand Registry','владелец, Claude'),
('февраль-март 2027','Листинги Amazon, A+ контент, FBA, старт продаж в марте','Claude'),
('март-апрель 2027','Менеджер криейторов и поддержка клиентов','владелец'),
('май 2027','Подтверждение у Vox объёма на год; SMP вторым источником','владелец'),
('август 2027','Ступень 5 000 по всем позициям, подготовка к Black Friday 2027','владелец')]
plan_tbl=tbl(['Срок','Действие','Кто'],plan,num=set())
ch1=yv('r_tt',1)/yv('rev',1); ch2=(yv('r_sf',1)+yv('r_ss',1))/yv('rev',1); ch3=yv('r_az',1)/yv('rev',1)

CSS=f'''@page{{size:A4;margin:15mm 14mm 16mm 14mm}}*{{box-sizing:border-box}}html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:"DejaVu Sans",sans-serif;font-size:8.7pt;line-height:1.45;color:{INK};margin:0}}
h1{{font-family:"DejaVu Serif",serif;font-size:24pt;line-height:1.12;margin:0 0 6pt}}
h2{{font-family:"DejaVu Serif",serif;font-size:14pt;margin:16pt 0 6pt;color:{ACC};border-bottom:.8pt solid {ACC};padding-bottom:3pt;page-break-after:avoid}}
h3{{font-size:9.8pt;margin:10pt 0 4pt;page-break-after:avoid}}p{{margin:0 0 5pt}}
.kicker{{font-size:7.4pt;letter-spacing:.14em;text-transform:uppercase;color:{MUT};font-weight:bold}}
.lede{{font-size:10.5pt;color:#33403b;margin:4pt 0 10pt}}
table{{width:100%;border-collapse:collapse;margin:3pt 0 8pt;font-size:7.9pt;page-break-inside:avoid}}
th{{background:#E2EEE8;text-align:left;padding:3.5pt 4pt;border-bottom:.8pt solid {ACC};vertical-align:bottom}}
td{{padding:3.2pt 4pt;border-bottom:.5pt solid {LINE};vertical-align:top}}td.n,th.n{{text-align:right;white-space:nowrap;font-family:"DejaVu Sans Mono",monospace}}
tr.total td{{font-weight:bold;background:#F1F5F2}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);border:.8pt solid {LINE};margin:6pt 0 10pt}}
.kpi{{padding:7pt 8pt;border-right:.6pt solid {LINE};border-bottom:.6pt solid {LINE}}}.kpi b{{display:block;font-family:"DejaVu Sans Mono",monospace;font-size:13pt;color:{ACC}}}.kpi span{{font-size:7.4pt;color:{MUT}}}
.callout{{border-left:2.4pt solid {C2};background:#FBF1E4;padding:6pt 9pt;margin:6pt 0 9pt}}
ul{{margin:0 0 6pt;padding-left:14pt}}li{{margin-bottom:2pt}}.pb{{page-break-before:always}}
.ax{{font-family:"DejaVu Sans",sans-serif;font-size:8.5px;fill:{MUT}}}.lab{{font-family:"DejaVu Sans Mono",monospace;font-size:8.5px;fill:{INK}}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:14pt}}.mut{{color:{MUT};font-size:7.6pt}}
.foot{{font-size:7pt;color:{MUT};border-top:.5pt solid {LINE};padding-top:5pt;margin-top:12pt}}'''
html=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>The Aldera: бизнес-план</title><style>{CSS}</style></head><body>
<div class="kicker">The Aldera · 518 GROUP LLC · бизнес-план · 03.10.2026</div>
<h1>Бизнес-план The Aldera</h1>
<p class="lede">Бренд добавок для США: четыре базовых продукта с понятным составом, продажи через криейторов TikTok Shop, подписку на Shopify и Amazon. Финансовая модель приложена отдельным файлом: Aldera_FinModel.xlsx.</p>

<h2>1. Резюме</h2>
<div class="kpis">
<div class="kpi"><b>${fm(20000+T2)}</b><span>вложение: $20 000 в октябре, ${fm(T2)} до 25 ноября</span></div>
<div class="kpi"><b>{K(B['rev1'])}</b><span>выручка года 1</span></div>
<div class="kpi"><b>{K(B['ebitda1'])}</b><span>EBITDA года 1, {P(B['ebitda1']/B['rev1'])} от выручки</span></div>
<div class="kpi"><b>{K(B['ebitda2'])}</b><span>EBITDA года 2</span></div>
<div class="kpi"><b>{MN[B['payback']]}</b><span>EBITDA перекрывает вложения</span></div>
<div class="kpi"><b>{MN[B['m1m']]}</b><span>темп $1 млн EBITDA в год</span></div>
<div class="kpi"><b>{fm(B['subs2'])}</b><span>подписчиков через 24 месяца</span></div>
<div class="kpi"><b>{('больше 99%' if mc['p_y2_1m']>0.99 else P(mc['p_y2_1m'],1))}</b><span>вероятность EBITDA года 2 от $1 млн (Монте-Карло)</span></div>
</div>
<ul>
<li><b>Что продаём.</b> Colostrum, Women's Probiotic, Magnesium Glycinate, Creatine. Производитель Vox Nutrition (Юта): площадка в реестре NSF/ANSI 455-2 как Manufacturing Facility, товар на складе, минимум 150 банок, этикетка копирует макет завода.</li>
<li><b>Кому.</b> Женщина 25-45, покупает добавки в TikTok Shop и на Amazon, устала от формул на 20 ингредиентов.</li>
<li><b>Как продаём.</b> 50 криейторов со старта, 8 роликов в месяц за 30% комиссии, рост до 150 к концу года 1 и до 400 к году 3. TikTok приводит покупателя, подписка на Shopify удерживает, Amazon ловит поиск с марта 2027.</li>
<li><b>Почему заработаем.</b> Подписчик приносит ${SUB_P:.0f} в месяц после всех расходов, в {str(round(SUB_P/FP_TT,1)).replace('.',',')} раза больше первой покупки в TikTok, и платит каждый месяц. Платная реклама только Spark Ads на ролики, которые уже выстрелили.</li>
<li><b>Что может помешать.</b> Главные риски: криейторы не выпускают ролики, конверсия ниже базы, подписка слабее плана. Даже в пессимистичном Монте-Карло (P10) EBITDA года 1 {K(mc['ebitda1']['p10'])}</li>
</ul>
<div class="callout"><b>Одно решение по деньгам.</b> При втором транше $5 000 и запасе товара 1,3 месяца денег в декабре 2026 не хватает на {M(-B['mincash'])}. По Монте-Карло при транше $5 000 денег не хватает в {P(mc['p_cash_neg'])} случаев; чтобы закрыть 90% исходов, нужно ещё {M(round(mc['need_p90'],-3))} сверх $5 000. Рекомендация: <b>второй транш ${fm(T2)} вместо $5 000</b>, всего ${fm(20000+T2)}. {('Без этого держать запас 1,0 месяца в декабре и перезаказывать дважды в месяц.' if A['funding'][1][1]>=0 else 'Запас 1,0 месяца проблему не снимает: нехватка всё равно '+M(-A['funding'][1][1])+'. Варианты: доплата владельца, отсрочка платежа у Vox на перезаказы, кредит под товар или рост медленнее спроса с потерей части продаж.')}</div>

<h2>2. Компания</h2>
{tbl(['Пункт','Данные'],[['Бренд','The Aldera'],['Юрлицо','518 GROUP LLC, Florida LLC, документ L26000430734, зарегистрирована 17.08.2026'],['Адрес','7901 4th St N, Suite 300, St. Petersburg, FL 33702 (Northwest Registered Agent)'],['Где на документах','Distributed by на этикетках, TikTok Shop Seller, Shopify Payments, Amazon, GS1, заявка на товарный знак'],['Производитель','Vox Nutrition Inc., 8224 Industry Circle, West Jordan, UT. Резерв: SMP Nutra, Largo, FL']],num=set())}

<h2>3. Продукт</h2>
{unit_tbl}
<p class="mut">Прибыль с банки после товара, комиссий, криейтора 30% (TikTok), доставки, склада $2.50 и возвратов. Amazon после 15% комиссии, FBA и рекламы 15% цены.</p>
<p><b>Почему эти четыре.</b> Высокий доказанный спрос и низкий риск по сырью и документам: подписанные спецификации Vox, без предупреждений Prop 65 на макетах. Отклонены электролит и ашваганда (Prop 65 на макете), Magnesium Complex (40% магния из оксида), Greens и Sea Moss (риск тяжёлых металлов), Omega 3 и Collagen (после комиссий нет прибыли), GLP1 и Berberine (держатся на заявлениях о болезни).</p>
<h3>Наборы и подписка</h3>
{tbl(['Предложение','Цена','Прибыль TikTok','Прибыль Shopify'],[[n,f"${o[0]:.2f}",f"${offer_profit(o[0],o[1],o[3],'tt'):.2f}",f"${offer_profit(o[0],o[1],o[3],'sh'):.2f}"] for n,o in zip(['Foundation: Colostrum + Magnesium','Gut Duo: Colostrum + Probiotic','The Daily Four'],OFF[:3])]+[[n,f"${o[0]:.2f}",'',f"${offer_profit(o[0],o[1],o[3],'sh'):.2f}"] for n,o in zip(['Подписка Foundation, в месяц','Подписка Gut Duo, в месяц','Подписка Daily Four, в месяц'],SUBS)])}

<h2 class="pb">4. Рынок и позиционирование</h2>
<p><b>Обещание:</b> Four basics. Nothing to decode. Четыре базовых продукта, нечего расшифровывать. Стоит под мастер-теглайном платформы бренда: <b>What you see is what you get.</b></p>
<div class="two"><div>
<h3>Для кого</h3><p>Женщина 25-45, покупает добавки в TikTok Shop и на Amazon. Устала от банок с 20 ингредиентами и обещаниями, которые нечем проверить. Упаковка нейтральная, креатин и магний покупают и мужчины, но голос бренда и криейторы женские.</p>
<h3>Чем отличаемся</h3><p>Рынок продаёт обещанием «моя жизнь изменилась». The Aldera продаёт цифрой: одно число крупно на лицевой стороне банки (2,000 mg colostrum · 400 mg IgG; 50 Billion CFU; 100% glycinate; 5 g creatine) и то же число на обороте.</p>
</div><div>
<h3>Цена в рынке</h3>{tbl(['Сегмент','Цена банки','Что продаёт'],[['Массовый Amazon','$15-25','цену за количество'],['<b>The Aldera</b>','<b>$30-40</b>','<b>проверяемую цифру</b>'],['Премиальный DTC','$50-100+','историю и обещание']],num={1})}
<h3>Ритуал дня</h3><p>Утро: Colostrum, Women's Probiotic, Creatine. Вечер: Magnesium Glycinate. Готовый сюжет для формата «моя рутина».</p>
</div></div>

<h2>5. Продажи по каналам</h2>
{tbl(['Канал','Роль','Механика','Доля выручки года 1'],[['TikTok Shop','приводит покупателя','криейторы 30% за 8 роликов: Flip the jar, утренняя рутина, «я убрала лишнее»',P(ch1)],['Shopify','удерживает','подписка на наборы, письма на 0, 7 и 25-й день, вкладыш с кодом',P(ch2)],['Amazon','ловит поиск и отзывы','с марта 2027: 5 продаж в день на продукт, через полгода 30, A+ контент «What’s inside»',P(ch3)]],num={3})}
<h3>Воронка одного криейтора в месяц</h3>
<p>8 роликов × {fm(VIEWS)} просмотров × 0,05% конверсии + 20% органики = {CR_ORD:.0f} заказа на {M(CR_ORD*50.8)}. Криейтор получает {M(CR_ORD*50.8*.3)} (около {M(CR_ORD*50.8*.3/8)} за ролик), бренд ${CR_ORD*FP_TT:.0f} с первых покупок и около {CR_ORD*1.1*.15:.0f} новых подписчиков на ${fm(CR_ORD*1.1*.15*SUB_P*10)} прибыли за их жизнь.</p>
<h3>Платная реклама: только Spark Ads на выстрелившие ролики</h3>
<p>Решение владельца: платим за рекламу только тех роликов криейторов, которые уже доказали продажи органически. Старт в феврале 2027, после декабрьского провала денег. В модели: 10% органической выручки TikTok, выручка на $1 рекламы (ROAS) 3 в базе.</p>
{tbl(['Правило','Порог','Почему'],[['Ролик считается выстрелившим','40 000 просмотров за 72 часа (втрое выше среднего) и 0,05% заказов от просмотров','это базовая конверсия модели, ролик её доказал'],['Держать рекламу','ROAS от 2','реклама окупается за 3 месяца за счёт подписчиков: безубыточность около 1,8'],['Масштабировать','ROAS от 4','окупается уже первой покупкой: безубыточность около 4'],['Выключить','ROAS ниже 2 семь дней подряд','не окупается и за 3 месяца']],num=set())}
<p class="mut">Безубыточность считана по модели: прибыль первой покупки TikTok {P(FP_TT/50.8)} от цены, подписчик за 3 месяца даёт ещё около 32% от цены первого заказа. Пороги просмотров это предложение, уточняется по первым неделям.</p>

<h2>6. Операции</h2>
<ul>
<li><b>Поставка.</b> Vox, сток, минимум 150 банок на позицию, цена по ступени объёма. Партия 1 в октябре: колострум 1 000, магний 1 000, пробиотик 400, креатин 200. Дальше перезаказ каждый месяц с запасом 1,3 месяца продаж.</li>
<li><b>Качество и этикетка.</b> Этикетка копирует макет Vox слово в слово, меняются только имя бренда и строка Distributed by. COA каждой партии.</li>
<li><b>Склад.</b> Склад-отправщик во Флориде, $2.50 за заказ, договор до старта: в декабре уже больше 35 заказов в день.</li>
<li><b>Юридическое.</b> Заявка USPTO на THE ALDERA (класс 5) до 10.10, GS1 и 4 GTIN, страховка ответственности.</li>
</ul>
<h3>Команда</h3>{team_tbl}

<h2 class="pb">7. Финансовый план</h2>
<p>Базовый сценарий. Модель помесячная на 36 месяцев, все формулы живые в Aldera_FinModel.xlsx. Платная реклама: Spark Ads на выстрелившие ролики с февраля 2027 (10% органической выручки TikTok, ROAS 3). Meta и Google не заложены. Комиссия TikTok 8%. Зарплата владельца не заложена.</p>
{chart_monthly()}
<h3>Отчёт о прибылях по годам</h3>
{pl_tbl}
<p class="mut">Год 1: ноябрь 2026 - октябрь 2027. Год 2 и 3 по тому же календарю. Налог 25% это оценка, уточнить у бухгалтера.</p>
<h3>Год 1 по кварталам</h3>
{q_tbl}
<h3>Деньги на старте</h3>
{fund_tbl}

<h2>8. Сценарии и риски</h2>
<h3>Три сценария</h3>
{sc_tbl}
<p class="mut">Консервативный: 10 700 просмотров на ролик у первых 50, 0,03% конверсии, 60% роликов, подписка 12%, отток 12%, Amazon 13 продаж в день. Оптимистичный: 17 500, 0,07%, подписка 20%, отток 8%, Amazon 45.</p>
<h3>Монте-Карло: {fm(A['mc_n'])} прогонов со случайными вводными</h3>
{mc_tbl}
{chart_hist()}
<p>EBITDA года 1 в минусе: {P(mc['p_y1_loss'])} прогонов. Темп $1 млн в год наступает к {mc['m1m_p50']}-му месяцу в медиане (от {mc['m1m_p10']}-го до {mc['m1m_p90']}-го).</p>
<h3>Что сильнее всего двигает прибыль второго года</h3>
{chart_tornado()}
<h3>Стресс-тесты</h3>
{st_tbl}
<p>Запас прочности большой: без Amazon EBITDA года 1 в плюсе уже при конверсии {str(round(A['be_conv_y1_noamz']*100,4)).replace('.',',')}%, это в 11 раз ниже базы.</p>
<h3>Главные риски</h3>
{risk_tbl}

<h2>9. План действий</h2>
{plan_tbl}

<h2>10. KPI для ежемесячного контроля</h2>
{tbl(['Показатель','Цель','Сигнал тревоги'],[['Роликов на криейтора в неделю','2','меньше 2 две недели подряд'],['Заказов на 1 000 просмотров','0,5','меньше 0,4 в первые 2 недели'],['Переход в подписку','15%','меньше 10% за 60 дней'],['Отток подписки','10% в месяц','больше 12%'],['Новых криейторов в месяц','10','меньше 8'],['Деньги на счёте','больше месячной закупки','меньше $3 000'],['Срок перезаказа Vox','до 15 рабочих дней','больше 15']],num=set())}

<div class="foot">Расчёт: финансовая модель Aldera_FinModel.xlsx (3 481 формула, сверена с Python-копией до цента), анализ сценариев, чувствительности и Монте-Карло: скрипты в папке finmodel репозитория. Цены поставщика: прайс Vox Nutrition 2026 Q3. Решения владельца на 03.10.2026: 4 продукта, вложение партиями, 50 криейторов за 30% и 8 роликов, этикетка по макету завода.</div>
</body></html>'''
open('business_plan.html','w').write(html)
CH='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
subprocess.run([CH,'--headless','--no-sandbox','--disable-gpu','--no-pdf-header-footer','--print-to-pdf=The Aldera - Business Plan.pdf','business_plan.html'],capture_output=True)
print('done')
