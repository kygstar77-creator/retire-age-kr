# H-4 보강(youtube-loop 2026-11-11): 철산동 84㎡대 전세 신규 vs 갱신 가운데 값 — calc.py와 같은 원자료(raw/rt, 2026-10-16 받음)
exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'calc.py'),encoding='utf-8').read().split("print('# H-4 calc_out")[0])
from collections import defaultdict
g=defaultdict(lambda: {'신규':[], '갱신':[]})
for r in R:
    if r['umdNm']=='철산동' and is84(r) and num(r.get('monthlyRent'))==0 and r.get('contractType') in ('신규','갱신'):
        g[(r['aptNm'],r['buildYear'])][r['contractType']].append(num(r['deposit']))
print('# 철산동 84㎡대 전세(월세 0) 신규·갱신 가운데 값, 둘 다 5건 이상')
for k,v in sorted(g.items(), key=lambda x:-med(x[1]['신규'])):
    if len(v['신규'])>=5 and len(v['갱신'])>=5:
        a,b=med(v['신규']),med(v['갱신'])
        print(f'- {k[0]}({k[1]}) 신규 {len(v["신규"])}건 {eok(a)} · 갱신 {len(v["갱신"])}건 {eok(b)} · 차 {eok(a-b)} · 섞으면 {eok(med(v["신규"]+v["갱신"]))}')
