import json,sys,datetime,collections,statistics as st
sys.stdout.reconfigure(encoding='utf-8')
O=json.load(open('cafes.json',encoding='utf-8'))
KST=datetime.timezone(datetime.timedelta(hours=9));now=datetime.datetime.now(KST).timestamp()*1000
poolR=collections.defaultdict(list)
for cid,c in O.items():
    A=c['arts']
    if not A: continue
    for a in A: a['t']=datetime.datetime.fromtimestamp(a['ts']/1000,KST)
    span=(A[0]['ts']-A[-1]['ts'])/864e5
    w=collections.Counter(a['nick'] for a in A)
    top=w.most_common(3)
    hrs=collections.Counter(a['t'].hour for a in A)
    print(f"\n## {c['name']} 글 {len(A)} / {span:.1f}일 = 하루 {len(A)/span:.1f}편 · 글쓴이 {len(w)}명")
    print(' 시간대별 글 비율(%):',' '.join(f"{h}:{hrs[h]*100/len(A):.0f}" for h in range(24)))
    for nick,n in top:
        mine=sorted([a for a in A if a['nick']==nick],key=lambda a:a['ts'])
        gaps=[(mine[i+1]['ts']-mine[i]['ts'])/6e4 for i in range(len(mine)-1)]
        days=collections.Counter(a['t'].date() for a in mine)
        hh=collections.Counter(a['t'].hour for a in mine)
        print(f"  글쓴이 {nick[:10]} lv{mine[0]['lv']}: {n}편 하루 {n/span:.1f} (최대 {max(days.values())}/일) 간격 중앙 {st.median(gaps) if gaps else 0:.0f}분 최소 {min(gaps) if gaps else 0:.0f}분 · 시각 {' '.join(f'{h}시{k}' for h,k in hh.most_common(5))}")
    # reads by hour for posts aged 1-5 days
    old=[a for a in A if 1<=(now-a['ts'])/864e5<=5]
    if len(old)>50:
        m=st.median(a['read'] for a in old) or 1
        g=collections.defaultdict(list)
        for a in old: g[a['t'].hour].append(a['read']/m)
        for h,x in g.items(): poolR[h]+=x
        print('  1~5일 된 글 조회 중앙',m, '| 시간대별 조회 배수:',' '.join(f"{h}:{st.median(x):.1f}" for h,x in sorted(g.items()) if len(x)>=5))
print('\n전체 카페 합친 시간대별 조회 배수(1~5일 글):',' '.join(f"{h}:{len(x)},{st.median(x):.2f}" for h,x in sorted(poolR.items())))
