import math, json
from model_daily_four import TIERS, PRICE, RET, SHIP, FBA, tier_cost, FIRST, SUBS, AMZ
SKUS=list(PRICE)
def offer_goods(it,cost): return sum(cost[s]*q for s,q in it.items())
def creators(m): return 50 if m<=2 else (50+10*(m-2) if m<=12 else 150+12*(m-12))
def demand(m,P):
    frac = 11/30 if m==1 else 1.0
    seas = 1.15 if m in (1,2) else (1.10 if m==3 else 1.0)
    per = 8*P['views']*P['conv']*P['delivery']
    tt = creators(m)*per*(1+P['org'])*frac*seas
    sd = P['direct']*tt
    az = (P['az0']+P['azstep']*(m-5)) if m>=5 else 0
    return tt,sd,az
def run(P,first,months=24,budget=20000,setup=2249,verbose=False):
    stock=dict(first); cost={s:tier_cost(s,first[s]) for s in SKUS}
    cash=budget-setup-sum(first[s]*tier_cost(s,first[s]) for s in SKUS)
    subs=0.0; carry=0.0; out=[]
    for m in range(1,months+1):
        tt,sd,az=demand(m,P)
        billed = out[-1]['subs_end'] if out else 0.0
        # demand units
        need={s:0.0 for s in SKUS}
        for n,p,it,sh,w in SUBS:
            for s,k in it.items(): need[s]+=billed*w*k
        for n,p,it,sh,w in FIRST:
            for s,k in it.items(): need[s]+=(tt+sd)*w*k
        for s,w in AMZ.items(): need[s]+=az*w
        fill={s:(min(1.0,stock[s]/need[s]) if need[s]>0 else 1.0) for s in SKUS}
        # subs filled first
        sub_need={s:sum(billed*w*it.get(s,0) for n,p,it,sh,w in SUBS) for s in SKUS}
        sfill={s:(min(1.0,stock[s]/sub_need[s]) if sub_need[s]>0 else 1.0) for s in SKUS}
        rem={s:stock[s]-sub_need[s]*sfill[s] for s in SKUS}
        oth={s:need[s]-sub_need[s] for s in SKUS}
        ofill={s:(min(1.0,rem[s]/oth[s]) if oth[s]>0 else 1.0) for s in SKUS}
        L=dict(rev={'tt':0,'sh':0,'az':0},goods=0,platform=0,creator=0,ship=0,returns=0,ppc=0,units={s:0.0 for s in SKUS},orders={'tt':0,'sh_first':0,'sh_sub':0,'az':0},lost=0.0)
        def sell(ch,q,p,it,sh,f):
            if q<=0: return
            qq=q*f; L['lost']+=(q-qq)*p
            L['rev'][ch]+=qq*p; L['goods']+=qq*offer_goods(it,cost); L['ship']+=qq*sh
            for s,k in it.items(): L['units'][s]+=qq*k
            if ch=='tt': L['platform']+=qq*.06*p; L['creator']+=qq*.30*p; L['returns']+=qq*.03*p
            elif ch=='sh': L['platform']+=qq*(.029*p+.30); L['returns']+=qq*.02*p
            return qq
        for n,p,it,sh,w in SUBS:
            f=min(sfill[s] for s in it); q=sell('sh',billed*w,p,it,sh,f); L['orders']['sh_sub']+=q or 0
        for n,p,it,sh,w in FIRST:
            f=min(ofill[s] for s in it)
            L['orders']['tt']+=sell('tt',tt*w,p,it,sh,f) or 0
            L['orders']['sh_first']+=sell('sh',sd*w,p,it,sh,f) or 0
        for s,w in AMZ.items():
            q=az*w*ofill[s]; p=RET[s]; L['lost']+=(az*w-q)*p
            L['rev']['az']+=q*p; L['goods']+=q*cost[s]; L['platform']+=q*(.15*p+FBA[s]); L['ppc']+=q*.20*p; L['units'][s]+=q; L['orders']['az']+=q
        for s in SKUS: stock[s]-=L['units'][s]
        fixed=500 if m<=12 else 1000
        L['ful']=P.get('ful',2.5)*(L['orders']['tt']+L['orders']['sh_first']+L['orders']['sh_sub'])
        L['ship']+=L['ful']
        rev=sum(L['rev'].values())
        profit=rev-L['goods']-L['platform']-L['creator']-L['ship']-L['returns']-L['ppc']-fixed
        # subscriptions: only customers who actually got first order
        first_orders=L['orders']['tt']+L['orders']['sh_first']
        subs_end=subs*(1-P['churn'])+first_orders*P['subconv']; subs=subs_end
        # cash: tt/az net 50% now 50% next month; shopify now
        net_tt=L['rev']['tt']*(1-.06-.30-.03)
        net_az=L['rev']['az']-sum(0 for _ in [0])  # gross
        net_az=L['rev']['az']-(L['platform']-(L['rev']['tt']*.06)-(L['rev']['sh']*0))  # placeholder fixed below
        az_fees=sum(0 for _ in [0])
        # recompute amazon fees directly
        azf=0
        for s,w in AMZ.items():
            q=az*w*ofill[s]; p=RET[s]; azf+=q*(.15*p+FBA[s]+.20*p)
        net_az=L['rev']['az']-azf
        net_sh=L['rev']['sh']*(1-.029-.02)-.30*(L['orders']['sh_sub']+L['orders']['sh_first'])
        now=.5*(net_tt+net_az)+net_sh
        cash+=carry+now-L['ship']-fixed; carry=.5*(net_tt+net_az)
        # reorder for next month, cover 1.3x next-month demand
        tt2,sd2,az2=demand(m+1,P)
        n2={s:0.0 for s in SKUS}
        for n,p,it,sh,w in SUBS:
            for s,k in it.items(): n2[s]+=subs_end*w*k
        for n,p,it,sh,w in FIRST:
            for s,k in it.items(): n2[s]+=(tt2+sd2)*w*k
        for s,w in AMZ.items(): n2[s]+=az2*w
        want={s:max(0,1.3*n2[s]-stock[s]) for s in SKUS}
        want={s:(0 if want[s]<1 else max(150,math.ceil(want[s]/50)*50)) for s in SKUS}
        bill=sum(want[s]*tier_cost(s,want[s]) for s in SKUS if want[s])
        spend_cap=max(0,cash-1000)  # keep $1k buffer
        scale=1.0 if bill<=spend_cap else (spend_cap/bill if bill>0 else 0)
        buy=0; bought={}
        for s in SKUS:
            q=want[s]*scale
            q=0 if q<150 else math.floor(q/50)*50
            if q:
                c=tier_cost(s,q); buy+=q*c; stock[s]+=q; bought[s]=q
                cost[s]=(cost[s]*0+c)
        cash-=buy
        out.append(dict(m=m,creators=creators(m),videos=creators(m)*8*P['delivery']*(11/30 if m==1 else 1),tt_dem=tt,orders=L['orders'],subs_end=subs_end,billed=billed,rev=L['rev'],goods=L['goods'],platform=L['platform'],creator=L['creator'],ship=L['ship'],ful=L['ful'],returns=L['returns'],ppc=L['ppc'],fixed=fixed,profit=profit,buy=buy,bought=bought,cash=cash,carry=carry,lost=L['lost'],units=L['units'],fill=ofill,stock=dict(stock)))
    return out
STD=dict(conv=0.0005,views=5000,delivery=1.0,org=0.20,direct=0.10,subconv=0.15,churn=0.10,az0=100,azstep=80)
FIRSTBUY={'COL':1000,'MG':1000,'PRO':400,'CRE':250}
if __name__=='__main__':
    o=run(STD,FIRSTBUY)
    for r in o:
        print(r['m'],r['creators'],round(r['orders']['tt']),round(r['subs_end']),round(sum(r['rev'].values())),round(r['profit']),round(r['buy']),round(r['cash']),'lost',round(r['lost']),{k:round(v,2) for k,v in r['fill'].items()})
