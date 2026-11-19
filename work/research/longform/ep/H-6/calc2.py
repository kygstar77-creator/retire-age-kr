"""H-6 가운데 값끼리(H-5 교훈: 최고 한 건 ↔ 지금 한 건은 잣대가 다름) — calc_out.txt(국토부 실거래 11/19, 해제 뺌)의 평형별 계약 기간 묶음 중앙값.
   + 회의 11/19 지시 '같은 높은 층 한 건끼리': 84㎡ 13층 43.10억(2025-10-31) ↔ 14층 35.00억(2026-10-31)."""
import re, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
t=open('calc_out.txt',encoding='utf-8').read()
G=[('2025.10~12',lambda d:d<'2026.01'),('2026.01~06',lambda d:'2026.01'<=d<'2026.07'),('2026.07~09',lambda d:'2026.07'<=d<'2026.10'),('2026.10~11',lambda d:d>='2026.10')]
for sec in ['77','84']:
    blk=t.split(f'## 전용 {sec}㎡')[1].split('##')[0]
    rows=[(m[0],float(m[1]),int(m[2])) for m in re.findall(r'(\d{4}\.\d\d\.\d\d) ([\d.]+)억 (\d+)층',blk)]
    meds=[]
    for lab,f in G:
        v=[p for d,p,fl in rows if f(d)]; meds.append(st.median(v))
        print(f'{sec}㎡ {lab}: {len(v)}건 가운데 {st.median(v):.2f}억 (최저 {min(v):.2f} 최고 {max(v):.2f})')
    print(f'{sec}㎡ 첫 묶음→끝 묶음 가운데 값 {meds[0]:.2f}→{meds[-1]:.2f}억 ({meds[-1]-meds[0]:+.2f}억, {meds[-1]/meds[0]*100:.0f}%)')
    hi=[(d,p,fl) for d,p,fl in rows if fl>=5]
    print(f'{sec}㎡ 5층 이상만: 최고 {max(hi,key=lambda x:x[1])} · 마지막 {hi[-1]}')
