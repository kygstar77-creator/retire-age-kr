# 국세청 근로소득 백분위(천분위) 2024년 귀속(2025 신고, data.go.kr 15082063 수정 2026-05-08) → 구간 평균 총급여(만원)
import csv, json, sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[]
for r in csv.reader(open('raw/nts_pct_utf8.csv',encoding='utf-8')):
    if not r or '상위' not in r[0]: continue
    k=r[0].strip(); n=int(r[1]); g=int(r[2])
    rows.append(dict(k=k,n=n,pay_eok=g,avg_man=round(g*1e8/n/1e4)))
tot_n=sum(r['n'] for r in rows if '.' not in r['k'] or r['k'].endswith('1.0%') and False)
pct=[r for r in rows if '.' not in r['k']]   # 상위 2%~100% 백분위
th=[r for r in rows if '.' in r['k']]       # 상위 0.1~1.0% 천분위
N=sum(r['n'] for r in pct)+sum(r['n'] for r in th)
G=sum(r['pay_eok'] for r in pct)+sum(r['pay_eok'] for r in th)
print('총인원',N,'총급여(억)',G,'평균(만원)',round(G*1e8/N/1e4))
for r in th: print(r['k'],r['n'],r['avg_man'])
for r in pct: print(r['k'],r['n'],r['avg_man'])
json.dump(dict(N=N,G_eok=G,rows=rows),open('nts_pct.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
