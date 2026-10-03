"""Collect public TikTok creator stats via the creator embed page (followers, likes, last ~10 videos with views).
Usage: python3 tt_stats.py handles.json out.jsonl   (resumable; skips handles already in out.jsonl)"""
import sys, json, re, time, random, subprocess, datetime, os
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
src, out = sys.argv[1], sys.argv[2]
H=json.load(open(src))
done=set()
if os.path.exists(out):
    for l in open(out):
        try: done.add(json.loads(l)['handle'].lower())
        except: pass
def fetch(h):
    r=subprocess.run(['curl','-s','--max-time','25','-A',UA,f'https://www.tiktok.com/embed/@{h}'],capture_output=True)
    s=r.stdout.decode('utf-8','ignore')
    m=re.search(r'<script id="__FRONTITY_CONNECT_STATE__"[^>]*>(.*?)</script>',s,re.S)
    if not m: return dict(handle=h,ok=False,err='nostate',size=len(s))
    d=json.loads(m.group(1)); data=d.get('source',{}).get('data',{})
    key=next((k for k in data if k.lower()==f'/embed/@{h}'.lower()),None)
    if not key: return dict(handle=h,ok=False,err='nokey')
    e=data[key]; ui=e.get('userInfo') or {}
    vids=[dict(id=v['id'],ts=int(v['id'])>>32,views=v.get('playCount'),desc=(v.get('desc') or '')[:160]) for v in (e.get('videoList') or [])]
    return dict(handle=h,ok=bool(ui),followers=ui.get('followerCount'),hearts=ui.get('heartCount'),following=ui.get('followingCount'),
                nickname=ui.get('nickname'),bio=(ui.get('signature') or '')[:300],verified=ui.get('verified'),videos=vids,fetched=datetime.datetime.utcnow().isoformat())
with open(out,'a') as f:
    for k,v in H.items():
        h=v['handle']
        if h.lower() in done: continue
        try: rec=fetch(h)
        except Exception as ex: rec=dict(handle=h,ok=False,err=str(ex)[:100])
        rec['meta']=v; f.write(json.dumps(rec,ensure_ascii=False)+'\n'); f.flush()
        time.sleep(1.2+random.random())
print('done')
