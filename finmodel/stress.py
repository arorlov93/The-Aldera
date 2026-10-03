import json
from twin import *
base=summary(run(params(2)))
ST=[('Базовый сценарий',{}),
 ('TikTok Shop заблокирован на 2 месяца (март-апрель 2027)',dict(tt_zero=(5,6))),
 ('Vox не отгрузил товар: месяц без продаж (февраль 2027)',dict(all_zero=(4,))),
 ('Amazon не дал допуск к категории',dict(amz_start=999)),
 ('Продукт не цепляет: конверсия 0,02%',dict(conv=0.0002)),
 ('Криейторов не прибавляется: 50 весь срок',dict(add1=0,add2=0)),
 ('Цены Vox +15%',dict(shock=1.15)),
 ('Подписка не работает: переход 5%, отток 15%',dict(subconv=.05,churn=.15)),
 ('Всё плохо сразу: конверсия 0,03%, 60% роликов, без Amazon, отток 12%',dict(conv=.0003,deliv=.6,amz_start=999,churn=.12,subconv=.12))]
out=[]
for lab,ov in ST:
    S=summary(run(params(2,**ov)))
    out.append(dict(lab=lab,e1=S['ebitda1'],e2=S['ebitda2'],e3=S['ebitda3'],mincash=S['mincash'],m1m=S['m1m']))
# break-even conversion without Amazon
def be(target,extra):
    lo,hi=0.000001,0.0008
    for _ in range(50):
        mid=(lo+hi)/2
        S=summary(run(params(2,conv=mid,**extra)))
        if target(S): hi=mid
        else: lo=mid
    return hi
r=json.load(open('analysis.json'))
r['stress']=out
r['be_conv_y1_noamz']=be(lambda S:S['ebitda1']>=0,dict(amz_start=999))
r['be_conv_y2_1m_noamz']=be(lambda S:S['ebitda2']>=1e6,dict(amz_start=999))
r['be_conv_y1_1m_noamz']=be(lambda S:S['ebitda1']>=1e6,dict(amz_start=999))
json.dump(r,open('analysis.json','w'),default=float,ensure_ascii=False,indent=1)
for o in out: print(o['lab'],round(o['e1']),round(o['e2']),round(o['mincash']),o['m1m'])
print(r['be_conv_y1_noamz'],r['be_conv_y2_1m_noamz'],r['be_conv_y1_1m_noamz'])
