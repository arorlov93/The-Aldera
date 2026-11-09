# Amazon unit economics, 2 products, price $29.99 per box
P=29.99
cogs={'Mg':3.73,'KSM':4.15}
ref=0.15*P; fba=3.20*1.035; stor=0.40; ret=0.03*P
def contrib(c,tacos): return P-ref-fba-stor-c-ret-tacos*P
print('per box before ads', {k:round(P-ref-fba-stor-c-ret,2) for k,c in cogs.items()})
for t in (0.40,0.30,0.20,0.15): print('TACoS',t,{k:round(contrib(c,t),2) for k,c in cogs.items()})
# scenarios units/day per product by month 1..12 and TACoS by month
tac=[0.45,0.40,0.35,0.30,0.25,0.22,0.20,0.18,0.16,0.15,0.15,0.15]
sc={'Осторожный':[1,1.5,2,2.5,3,3.5,4,4,4.5,5,5,5],
    'Базовый':[2,3,4,6,7,8,9,10,11,12,12,13],
    'Сильный':[3,5,8,11,14,17,20,22,24,26,28,30]}
fixed=40+100+100 # seller pro, tools, insurance (estimate)
one_off=2*200+2*1000 # Vine per ASIN + TIC verification per product (estimate)
for name,u in sc.items():
    rev=prof=0; units=0
    for m in range(12):
        n=u[m]*30*2
        units+=n; rev+=n*P
        prof+=sum(u[m]*30*contrib(c,tac[m]) for c in cogs.values())-fixed
    prof-=one_off
    print(name,'units',int(units),'revenue',round(rev),'profit',round(prof),'month12/day/product',u[11], 'm12 profit', round(sum(u[11]*30*contrib(c,tac[11]) for c in cogs.values())-fixed))
# breakeven TACoS
for k,c in cogs.items(): print('breakeven TACoS',k, round((P-ref-fba-stor-c-ret)/P,3))
