# calc.py 보조 — 달별 건수(10월 신고 덜 들어옴 확인)·8~9월만·보증금 구간별 월세 중간. 11/24 write-b
import json, os, glob, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
def n(s): return int((s or '0').replace(',', '') or 0)
by = {}
for f in glob.glob(os.path.join(H, 'raw', '*_rent.json')):
    ym = os.path.basename(f).split('_')[1]
    by.setdefault(ym, []).extend(json.load(open(f, encoding='utf-8')))
for ym in sorted(by):
    mon = [n(r['monthlyRent']) for r in by[ym] if n(r['monthlyRent']) > 0]
    print(ym, '전체', len(by[ym]), '월세', len(mon), f'몫 {len(mon)/len(by[ym])*100:.1f}%', '중간', st.median(mon), f'100↑ {sum(x>=100 for x in mon)/len(mon)*100:.1f}%')
for y in ('2025', '2026'):
    rows = by[y+'08'] + by[y+'09']
    mon = [r for r in rows if n(r['monthlyRent']) > 0]; m = [n(r['monthlyRent']) for r in mon]
    print(f'{y} 8~9월만: 월세 {len(m):,} 몫 {len(m)/len(rows)*100:.1f}% 중간 {st.median(m)} 100↑ {sum(x>=100 for x in m)/len(m)*100:.1f}%')
    rows3 = by[y+'08'] + by[y+'09'] + by[y+'10']; mon3 = [r for r in rows3 if n(r['monthlyRent']) > 0]
    for lo, hi, nm in ((0, 5000, '보증금 5천만원 이하'), (5001, 20000, '5천만원 넘고 2억 이하'), (20001, 10**9, '2억 넘음')):
        mm = [n(r['monthlyRent']) for r in mon3 if lo <= n(r['deposit']) <= hi]
        print(f'  {y} 8~10월 {nm}: {len(mm):,}건 ({len(mm)/len(mon3)*100:.1f}%) 중간 {st.median(mm)} 100↑ {sum(x>=100 for x in mm)/len(mm)*100:.1f}%')
