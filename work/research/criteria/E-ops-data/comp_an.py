import json,datetime,statistics as st,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
R=json.load(open('comp.json',encoding='utf-8'))
KST=datetime.timezone(datetime.timedelta(hours=9))
now=datetime.datetime.now(KST)
allS=collections.defaultdict(list); allL=collections.defaultdict(list)
for cid,c in R.items():
    vs=[v for v in c['vids'] if v['sec']>0]
    if not vs: continue
    for v in vs: v['t']=datetime.datetime.fromisoformat(v['pub'].replace('Z','+00:00')).astimezone(KST)
    vs=[v for v in vs if (now-v['t']).days>=2]
    S=[v for v in vs if v['sec']<=180]; L=[v for v in vs if v['sec']>180]
    span=max(1,(now-min(v['t'] for v in vs)).days)
    def hrs(xs):
        c=collections.Counter(v['t'].hour for v in xs); return ' '.join(f'{h}시{n}' for h,n in c.most_common(4))
    def mins(xs):
        c=collections.Counter(v['t'].strftime('%H:%M') for v in xs); return ' '.join(f'{k}×{n}' for k,n in c.most_common(3))
    perday=collections.Counter(v['t'].date() for v in S)
    print(f"{c['title'][:16]:16} 구독{int(c['subs'] or 0)//1000}k {span}일 | 롱폼 주{len(L)/span*7:.1f}편 [{hrs(L)}] [{mins(L)}] | 쇼츠 하루{len(S)/span:.2f}편 최대{max(perday.values()) if perday else 0} [{hrs(S)}] [{mins(S)}]")
    # within-channel: views relative to channel median by hour bucket
    for xs,agg in ((S,allS),(L,allL)):
        if len(xs)<5: continue
        m=st.median(v['views'] for v in xs) or 1
        for v in xs: agg[v['t'].hour].append(v['views']/m)
for nm,agg in (('쇼츠',allS),('롱폼',allL)):
    print(nm,'시각별 (편수, 채널 중앙 대비 배수 중앙)')
    print(' '.join(f'{h}시:{len(x)},{st.median(x):.2f}' for h,x in sorted(agg.items())))
