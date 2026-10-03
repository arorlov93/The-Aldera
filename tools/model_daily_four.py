import json, math, sys
TIERS=[150,300,500,1000,2500,5000,7500,10000]
PRICE={ # Vox price sheet, per tier
 'COL':[8.52,8.37,8.12,7.97,7.82,7.67,7.42,7.12],
 'MG': [5.51,5.16,4.81,4.61,4.41,4.11,3.91,3.76],
 'CRE':[6.90,6.75,6.50,6.35,6.20,6.05,5.80,5.50],
 'PRO':[8.34,7.99,7.64,7.44,7.24,6.94,6.74,6.59],
}
RET={'COL':39.95,'PRO':34.95,'MG':29.95,'CRE':29.95}
SHIP={'COL':4.50,'PRO':3.50,'MG':3.50,'CRE':5.50}
FBA={'COL':6.55,'PRO':5.40,'MG':5.40,'CRE':6.55}
def tier_cost(sku,qty):
    i=0
    for k,t in enumerate(TIERS):
        if qty>=t: i=k
    return PRICE[sku][i]
# offers: (name, price, items dict sku->jars, ship)
FIRST=[('Foundation',59.95,{'COL':1,'MG':1},5.50,.35),
       ('Gut Duo',64.95,{'COL':1,'PRO':1},5.50,.10),
       ('Daily Four',114.95,{'COL':1,'PRO':1,'MG':1,'CRE':1},8.50,.05),
       ('Colostrum',39.95,{'COL':1},4.50,.20),
       ('Probiotic',34.95,{'PRO':1},3.50,.12),
       ('Magnesium',29.95,{'MG':1},3.50,.10),
       ('Creatine',29.95,{'CRE':1},5.50,.08)]
SUBS=[('Foundation',54.95,{'COL':1,'MG':1},5.50,.60),
      ('Gut Duo',59.95,{'COL':1,'PRO':1},5.50,.25),
      ('Daily Four',99.95,{'COL':1,'PRO':1,'MG':1,'CRE':.5},7.50,.15)]
AMZ={'COL':.35,'MG':.25,'CRE':.25,'PRO':.15}
def econ(price,items,ship,cost,ch):
    goods=sum(cost[s]*q for s,q in items.items())
    if ch=='tt': fee=.06*price; cr=.30*price; ret=.03*price
    elif ch=='sh': fee=.029*price+.30; cr=0; ret=.02*price
    return price-goods-fee-cr-ship-ret, goods
def amz(sku,cost):
    p=RET[sku]; return p-cost[sku]-.15*p-FBA[sku]-.20*p
def run(conv=0.0003,views=3500,delivery=0.60,subconv=0.12,churn=0.08,org=0.10,months=24,amz_on=True):
    out=[]; subs=0.0; cash=21000-13136
    inv={'COL':500,'MG':500,'CRE':300,'PRO':300}
    cost={s:tier_cost(s,1000) for s in PRICE}
    for m in range(1,months+1):
        cr = 50 if m<=2 else (50+10*(m-2) if m<=12 else 150+12*(m-12))
        frac = 11/30 if m==1 else 1.0
        tt = cr*8*views*conv*delivery*(1+org)*frac
        if m in (1,2): tt*=1.15  # BFCM / gift season
        sdirect = .05*tt
        az = (30+50*(m-5)) if (amz_on and m>=5) else 0
        newsubs=(tt+sdirect)*subconv
        subs = subs*(1-churn)+newsubs
        # units
        units={s:0.0 for s in PRICE}
        rev={'tt':0,'sh':0,'az':0}; prof={'tt':0,'sh':0,'az':0}
        for n,p,it,sh,w in FIRST:
            q=tt*w; e,_=econ(p,it,sh,cost,'tt'); rev['tt']+=q*p; prof['tt']+=q*e
            qd=sdirect*w; e2,_=econ(p,it,sh,cost,'sh'); rev['sh']+=qd*p; prof['sh']+=qd*e2
            for s,k in it.items(): units[s]+= (q+qd)*k
        subs_billed = subs*(1-churn/2) if m>1 else 0  # new subs pay next month
        subs_billed = (out[-1]['subs'] if out else 0)
        for n,p,it,sh,w in SUBS:
            q=subs_billed*w; e,_=econ(p,it,sh,cost,'sh'); rev['sh']+=q*p; prof['sh']+=q*e
            for s,k in it.items(): units[s]+=q*k
        for s,w in AMZ.items():
            q=az*w; rev['az']+=q*RET[s]; prof['az']+=q*amz(s,cost); units[s]+=q
        fixed = 500 if m<=12 else 1000
        total=sum(prof.values())-fixed
        # reorder: keep 1.5 months of this month's demand after sales; buy at tier of order qty
        buy=0
        for s in PRICE:
            inv[s]-=units[s]
            target=1.5*units[s]
            if inv[s]<target:
                q=max(150, math.ceil((target-inv[s]+units[s])/50)*50)
                c=tier_cost(s,q); buy+=q*c; inv[s]+=q
                cost[s]=c if q>=1000 else cost[s]
        # cash: profit already nets COGS at cost; cash out = purchases, cash in = profit + goods cost of sold units
        cogs=sum(units[s]*cost[s] for s in PRICE)
        cash += total + cogs - buy
        out.append(dict(m=m,creators=cr,tt=tt,sd=sdirect,az=az,subs=subs,billed=subs_billed,units=units,rev=rev,prof=prof,fixed=fixed,total=total,buy=buy,cash=cash,cost=dict(cost)))
    return out
if __name__=='__main__':
    o=run()
    for r in o:
        print(r['m'],r['creators'],round(r['tt']),round(r['subs']),round(r['az']),{k:round(v) for k,v in r['units'].items()},round(sum(r['rev'].values())),round(r['total']),round(r['buy']),round(r['cash']))
