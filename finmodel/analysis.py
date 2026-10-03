import random, json, statistics
from twin import *
res={}
# scenarios
for s,n in ((1,'cons'),(2,'base'),(3,'opt')):
    res['scen_'+n]=summary(run(params(s)))
# funding variants (base)
fv=[]
import math
_b=summary(run(params(2)))
T2B=int(math.ceil((-_b['mincash']+5000)/1000.0)*1000) if _b['mincash']<0 else 5000
for lab,ov in (('Транш 2 = $5 000, запас 1,3 мес.',{}),('Транш 2 = $5 000, запас 1,0 мес.',dict(cover=1.0)),(f'Транш 2 = ${T2B:,} (база без нехватки)'.replace(',',' '),dict(t2=T2B))):
    S=summary(run(params(2,**ov))); fv.append((lab,S['mincash'],S['mincash_m'],S['ebitda1']))
res['funding']=fv
for s,n in ((1,'cons'),(3,'opt')):
    pass
# tornado on Y2 EBITDA and min cash
base=summary(run(params(2)))
TOR=[('v1','Просмотры: первые 50 криейторов',10700,17500),('v2','Просмотры: криейторы 51-200',6300,9400),('v3','Просмотры: криейторы 201+',450,2000),('conv','Конверсия просмотра в заказ',.0003,.0007),('deliv','Доля вышедших роликов',.6,1.0),
     ('subconv','Переход в подписку',.12,.20),('churn','Отток подписки',.12,.08),('add2','Новых криейторов в мес. с 13-го',6,18),('add1','Новых криейторов в мес. 3-12',5,15),
     ('azpeak','Amazon: продаж в день на продукт',13,45),('ppc','Amazon: доля рекламы',.20,.12),('sroas','Spark Ads: ROAS',2,4),('shock','Цена Vox',1.10,0.95),('cr_pct','Комиссия криейтора',.35,.25),('org','Органика',.10,.30)]
tor=[]
for k,lab,lo,hi in TOR:
    a=summary(run(params(2,**{k:lo}))); b=summary(run(params(2,**{k:hi})))
    tor.append((lab,lo,hi,a['ebitda2'],b['ebitda2'],a['ebitda1'],b['ebitda1']))
tor.sort(key=lambda t: -abs(t[4]-t[3]))
res['tornado']=tor; res['base']=base
# break-evens
def bisect_param(k,target_fn,lo,hi,it=40):
    for _ in range(it):
        mid=(lo+hi)/2
        if target_fn(summary(run(params(2,**{k:mid})))): hi=mid
        else: lo=mid
    return hi
res['be_conv_y1']=bisect_param('conv',lambda S:S['ebitda1']>=0,0.00001,0.0005)
res['be_conv_1m_y2']=bisect_param('conv',lambda S:S['ebitda2']>=1e6,0.00001,0.0005)
res['be_subconv_1m_y2_cons']=None
# Monte Carlo
random.seed(42)
N=5000; MC=[]
DIST={'v1':(8000,12700,20000),'v2':(5000,7800,11000),'v3':(300,560,2000),'conv':(.0002,.0005,.0008),'deliv':(.5,.85,1.0),'org':(.05,.2,.3),'direct':(.05,.1,.15),'subconv':(.08,.15,.22),
      'churn':(.07,.10,.15),'add1':(4,10,15),'add2':(5,12,18),'azpeak':(8,30,45),'azgrow':(0,1.5,2.5),'ppc':(.12,.15,.25),'sroas':(1.5,3,5),'shock':(.95,1.0,1.15)}
for i in range(N):
    ov={k:random.triangular(a,c,b) for k,(a,b,c) in DIST.items()}
    S=summary(run(params(2,**ov)))
    MC.append(S)
def pct(xs,p):
    xs=sorted(xs); return xs[int(p*(len(xs)-1))]
mc={}
for k in ('ebitda1','ebitda2','ebitda3','rev1','rev2','rev3','subs2','mincash'):
    xs=[s[k] for s in MC]; mc[k]=dict(p10=pct(xs,.10),p50=pct(xs,.5),p90=pct(xs,.9),mean=statistics.mean(xs))
mc['p_y1_loss']=sum(s['ebitda1']<0 for s in MC)/N
mc['p_y2_1m']=sum(s['ebitda2']>=1e6 for s in MC)/N
mc['p_y1_1m']=sum(s['ebitda1']>=1e6 for s in MC)/N
mc['p_cash_neg']=sum(s['mincash']<0 for s in MC)/N
mc['p_cash_neg10k']=sum(s['mincash']<-10000 for s in MC)/N
mc['need_p90']=-pct([s['mincash'] for s in MC],.10)
m1=[s['m1m'] if s['m1m'] else 99 for s in MC]
mc['m1m_p50']=pct(m1,.5); mc['m1m_p10']=pct(m1,.1); mc['m1m_p90']=pct(m1,.9); mc['p_m1m_within24']=sum(x<=24 for x in m1)/N
# histogram of Y2 EBITDA
bins=[-1e9,0,5e5,1e6,2e6,3e6,4e6,5e6,1e12]; labs=['убыток','$0-0,5 млн','$0,5-1 млн','$1-2 млн','$2-3 млн','$3-4 млн','$4-5 млн','больше $5 млн']
h=[0]*8
for s in MC:
    for j in range(8):
        if bins[j]<=s['ebitda2']<bins[j+1]: h[j]+=1; break
mc['hist_y2']=list(zip(labs,[x/N for x in h]))
res['mc']=mc; res['mc_dist']=DIST; res['mc_n']=N
json.dump(res,open('analysis.json','w'),default=float,ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in res.items() if k not in('mc_dist',)},default=lambda x: round(x) if isinstance(x,float) else x,ensure_ascii=False)[:6000])
