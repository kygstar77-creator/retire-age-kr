import json,datetime,statistics as st,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
V={v['id']:v for v in json.load(open('own_videos.json',encoding='utf-8'))};D=json.load(open('own_daily.json'))
W=r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research'
sh={json.loads(l)['id'] for l in open(W+r'\cardshorts\log.jsonl',encoding='utf-8') if l.strip()}
lg={json.loads(l)['videoId'] for l in open(W+r'\longform\loop\uploads.jsonl',encoding='utf-8') if l.strip()}
KST=datetime.timezone(datetime.timedelta(hours=9));PT=datetime.timezone(datetime.timedelta(hours=-7))
now=datetime.datetime.now(KST)
g=collections.defaultdict(list)
for i,v in V.items():
    if v['privacy']!='public': continue
    kind='S' if i in sh or (v['sec']<=60) else ('L' if i in lg or v['sec']>180 else '?')
    p=datetime.datetime.fromisoformat(v['pub'].replace('Z','+00:00'))
    k=p.astimezone(KST); d0=p.astimezone(PT).date()
    dd={r[0]:r[1] for r in D.get(i,[])} if not isinstance(D.get(i),str) else {}
    a2=sum(dd.get((d0+datetime.timedelta(days=j)).isoformat(),0) for j in range(3))
    age=(now-k).total_seconds()/3600
    band=f'{k.hour:02d}시'
    g[(kind,band)].append((k.strftime('%m-%d %H:%M'),a2,v['views'],round(age),i))
for key in sorted(g):
    xs=g[key]; ok=[x for x in xs if x[3]>=72]
    print(key,len(xs),'72h+:',len(ok),'| 첫3PT일 중앙',st.median([x[1] for x in ok]) if ok else '-','| 누적 중앙',st.median([x[2] for x in ok]) if ok else '-')
    for x in xs: print('   ',x)
