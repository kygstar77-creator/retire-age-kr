# pyeongchon1120 보조 계산 — 2021 상반기 vs 하반기(고점 근거), 단지 수 · calc.py와 같은 정의
import json, glob, statistics as st, collections as C, sys
sys.stdout.reconfigure(encoding='utf-8')
num=lambda s: float(str(s or '0').replace(',','') or 0)
rows=[]
for p in glob.glob('raw/*_trade.json'):
    for r in json.load(open(p,encoding='utf-8')):
        if r.get('cdealType') or r['umdNm'] not in('평촌동','호계동'): continue
        r['_ym']=int(r['dealYear'])*100+int(r['dealMonth']); r['_p']=num(r['dealAmount']); r['_k']=(r['umdNm'],r.get('aptSeq') or r['aptNm'],round(num(r['excluUseAr']))); rows.append(r)
for g in ('평촌동','호계동'):
    d=C.defaultdict(lambda:C.defaultdict(list))
    for r in rows:
        if r['umdNm']!=g: continue
        if 202101<=r['_ym']<=202106: d[r['_k']]['a'].append(r['_p'])
        if 202107<=r['_ym']<=202112: d[r['_k']]['b'].append(r['_p'])
    rs=[st.median(v['b'])/st.median(v['a'])-1 for v in d.values() if v['a'] and v['b']]
    print(g,'2021상→2021하',len(rs),'쌍',f'{st.median(rs)*100:+.1f}%')
    # 같은 집 짝 중 최근>고점인 단지 수(단지 단위)
print('단지 수', {g: len({r['aptNm'] for r in rows if r['umdNm']==g}) for g in('평촌동','호계동')})
