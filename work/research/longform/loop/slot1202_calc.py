# 12/2 롱폼 칸 후보 — 노도강(노원 11350·도봉 11320·강북 11305) 실거래로 경쟁 주장 맞대기 (youtube-loop 2026-11-22)
# 재료: work/research/rt/<구>_<월>_trade.json (국토교통부 아파트 매매 실거래, rtmolit.py 11/22 받음) · 해제·공공기관 매수 뺌 · 단위 억
# 묻는 것: ① '거래 끊겼다?'(아파트사이클 11/12·11/16) — 월별 건수 ② '노원은 신고가'(KBS 11/06) — 2026년에 2021년 이후 최고가를 넘긴 단지·면적
#          ③ 2021 고점 대비 지금 — 같은 단지·같은 면적(전용 ㎡ 반올림)의 2021년 최고 vs 2026-07~11 중앙
import json, os, glob, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
RT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'rt')
GU = {'11350': '노원구', '11320': '도봉구', '11305': '강북구'}
def num(s): return float(str(s or '0').replace(',', '') or 0) / 10000
rows = []
for code, gname in GU.items():
    for p in sorted(glob.glob(os.path.join(RT, f'{code}_*_trade.json'))):
        if 'offi' in p: continue
        try: d = json.load(open(p, encoding='utf-8'))
        except Exception: continue
        for r in d:
            if not isinstance(r, dict) or 'aptNm' not in r: continue
            if r.get('cdealType') or r.get('buyerGbn') == '공공기관': continue
            ym = f"{r['dealYear']}{str(r['dealMonth']).zfill(2)}"
            rows.append(dict(gu=gname, apt=(r.get('aptNm') or '').strip(), dong=r.get('umdNm'), a=round(float(r['excluUseAr'])),
                             ym=ym, day=int(r['dealDay']), amt=num(r['dealAmount']), gbn=r.get('dealingGbn', ''), by=r.get('buildYear')))
print(f'# 노도강 아파트 매매 {len(rows)}건 · 계약월 {min(r["ym"] for r in rows)}~{max(r["ym"] for r in rows)} (해제·공공기관 매수 뺌)')
print('\n## ① 월별 건수 (구별 / 합)')
c = collections.defaultdict(collections.Counter)
for r in rows: c[r['ym']][r['gu']] += 1
for ym in sorted(c):
    if ym >= '202101': print(ym, ' · '.join(f"{g} {c[ym][g]}" for g in GU.values()), '· 합', sum(c[ym].values()))
yr = collections.Counter(r['ym'][:4] for r in rows)
print('연도 합', dict(sorted(yr.items())))
print('\n## ③ 같은 단지·같은 면적: 2021년 최고가 vs 2026-07~11 중앙 (2026-07~11 거래 3건 이상인 묶음)')
g = collections.defaultdict(list)
for r in rows: g[(r['gu'], r['dong'], r['apt'], r['a'])].append(r)
res = []
for k, v in g.items():
    p21 = [r['amt'] for r in v if r['ym'][:4] == '2021']
    now = [r['amt'] for r in v if '202607' <= r['ym'] <= '202611']
    if p21 and len(now) >= 3:
        res.append((k, max(p21), st.median(now), len(now), st.median(now) / max(p21)))
res.sort(key=lambda x: -x[3])
rat = [x[4] for x in res]
print(f'묶음 {len(res)}개 · 지금/2021최고 가운데 {st.median(rat)*100:.1f}% · 넘은 묶음 {sum(1 for x in rat if x>=1)}개 · 80% 밑 {sum(1 for x in rat if x<0.8)}개')
for gname in GU.values():
    rr = [x[4] for x in res if x[0][0] == gname]
    if rr: print(f'  {gname}: 묶음 {len(rr)} · 가운데 {st.median(rr)*100:.1f}% · 범위 {min(rr)*100:.0f}~{max(rr)*100:.0f}%')
for x in res[:15]:
    (gu, dong, apt, a), mx, md, n, q = x
    print(f'  {gu} {dong} {apt} {a}㎡ · 2021 최고 {mx:.2f} · 2026-07~11 중앙 {md:.2f}({n}건) · {q*100:.1f}%')
print('\n## ② 2026년 신고가: 2026년 거래가 그 묶음의 2021-01~2025-12 최고가를 넘은 것')
hi = []
for k, v in g.items():
    before = [r['amt'] for r in v if r['ym'] < '202601']
    new = [r for r in v if r['ym'] >= '202601']
    if before and new:
        top = max(before); over = [r for r in new if r['amt'] > top]
        if over: hi.append((k, top, max(r['amt'] for r in over), len(over), min(r['ym'] for r in over)))
print(f'신고가 묶음 {len(hi)}개 (2026년 거래가 있는 묶음 {sum(1 for k,v in g.items() if any(r["ym"]>="202601" for r in v) and any(r["ym"]<"202601" for r in v))}개 중)')
for gname in GU.values(): print(f'  {gname}: {sum(1 for x in hi if x[0][0]==gname)}개')
for x in sorted(hi, key=lambda x: -x[3])[:12]:
    (gu, dong, apt, a), top, mx, n, ym = x
    print(f'  {gu} {dong} {apt} {a}㎡ · 이전 최고 {top:.2f} → 2026 {mx:.2f} ({n}건, 처음 {ym})')
m = collections.Counter(x[4] for x in hi); print('  처음 넘은 달', dict(sorted(m.items())))
