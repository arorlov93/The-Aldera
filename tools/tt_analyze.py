"""Compute per-creator view metrics from tt_stats output."""
import json, sys, statistics, re, time
NOW=time.time()
KW={'Колострум':r'colostrum','Пробиотик':r'probiotic|vaginal|ph balance|\bbv\b|gut health|bloat','Магний':r'magnesium','Креатин':r'creatine',
    'Добавки':r'supplement|vitamin|wellness|#ad\b|partner|tiktokshop|tiktokmademebuyit|creatorpicks|yellow basket'}
SELL=re.compile(r'#ad\b|#sponsored|partner|#tiktokshop|tiktokmademebuyit|creatorpicks|code |discount|link in bio|yellow basket|#affiliate',re.I)
def analyze(rec):
    v=[x for x in rec.get('videos',[]) if x.get('views') is not None]
    if not v: return None
    newest=max(x['ts'] for x in v)
    recent=[x for x in v if x['ts']>=newest-90*86400]          # drop old pinned
    recent.sort(key=lambda x:-x['ts'])
    mature=[x for x in recent if NOW-x['ts']>=3*86400] or recent
    views=[x['views'] for x in mature]
    span=(recent[0]['ts']-recent[-1]['ts'])/86400 if len(recent)>1 else 0
    ppm=min(60,(len(recent)-1)/max(span,1)*30) if len(recent)>1 else 0
    med=statistics.median(views)
    txt=' '.join(x['desc'] for x in recent).lower()
    return dict(handle=rec['handle'],followers=rec.get('followers') or 0,hearts=rec.get('hearts') or 0,n=len(recent),
        days_since=round((NOW-newest)/86400,1),posts_month=round(ppm,1),median_views=int(med),mean_views=int(statistics.mean(views)),
        max_views=max(views),share10k=round(sum(1 for x in views if x>=10000)/len(views),2),monthly_views=int(med*ppm),
        view_rate=round(med/max(rec.get('followers') or 1,1),3),sells=sum(1 for x in recent if SELL.search(x['desc'])),
        topics={k:sum(1 for x in recent if re.search(p,x['desc'],re.I)) for k,p in KW.items()},
        bio=rec.get('bio',''),email=bool(re.search(r'@[a-z0-9-]+\.[a-z]{2,}|✉|email|gmail',(rec.get('bio') or '').lower())),
        src=rec.get('meta',{}).get('src'),niche=rec.get('meta',{}).get('niche'),tier=rec.get('meta',{}).get('tier'))
if __name__=='__main__':
    out=[]
    for f in sys.argv[1:-1]:
        for l in open(f):
            r=json.loads(l)
            if r.get('ok'):
                a=analyze(r)
                if a: out.append(a)
    json.dump(out,open(sys.argv[-1],'w'),ensure_ascii=False); print(len(out))
