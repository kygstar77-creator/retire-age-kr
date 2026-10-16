# 상도동 84㎡대(전용 80~85㎡) 단지별·옆 동네 비교 — 국토부 실거래 원자료(work/research/rt/11590_*)만 쓴다
import json, glob, os, statistics as st, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
RT = os.path.join(os.path.dirname(__file__), '..', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
def rows(months):
    out = []
    for m in months:
        f = os.path.join(RT, f'11590_{m}_trade.json')
        if os.path.exists(f):
            d = json.load(open(f, encoding='utf-8')); out += d if isinstance(d, list) else d.get('rows', [])
    return [r for r in out if not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and 80 <= num(r['excluUseAr']) < 85]
LAST = [f'2025{m:02d}' for m in (11, 12)] + [f'2026{m:02d}' for m in range(1, 11)]
OLD = ['202110', '202111', '202112']
R, O = rows(LAST), rows(OLD)
print('기간', LAST[0], '~', LAST[-1], '· 84㎡대 거래', len(R))
# 동네별(옆 동네 비교)
print('\n[동별 84㎡대 1년 가운데 값, 억]')
by = collections.defaultdict(list)
for r in R: by[r['umdNm']].append(num(r['dealAmount']))
for k, v in sorted(by.items(), key=lambda x: -st.median(x[1])):
    if len(v) >= 10: print(f'  {k:6} {st.median(v)/1e4:6.2f}억 ({len(v)}건)')
# 상도동 단지별
print('\n[상도동 단지별 84㎡대 1년 가운데 값 · 2021년 10~12월 가운데 값]')
cur = collections.defaultdict(list); old = collections.defaultdict(list); last = {}
for r in R:
    if r['umdNm'] == '상도동':
        cur[r['aptNm']].append(num(r['dealAmount']))
        ym = r['dealYear'] + r['dealMonth'].zfill(2) + r['dealDay'].zfill(2)
        if r['aptNm'] not in last or ym > last[r['aptNm']][0]: last[r['aptNm']] = (ym, num(r['dealAmount']), r.get('floor'), r.get('buildYear'))
for r in O:
    if r['umdNm'] == '상도동': old[r['aptNm']].append(num(r['dealAmount']))
for k, v in sorted(cur.items(), key=lambda x: -st.median(x[1])):
    if len(v) < 3: continue
    o = old.get(k)
    om = f'{st.median(o)/1e4:.2f}억({len(o)}건) → {(st.median(v)/st.median(o)-1)*100:+.1f}%' if o and len(o) >= 2 else '-'
    print(f'  {k:16} 준공{last[k][3]} {st.median(v)/1e4:6.2f}억 ({len(v)}건) · 최근 {last[k][0]} {last[k][1]/1e4:.2f}억 {last[k][2]}층 · 2021말 {om}')
# 1년 전 같은 석 달(2025.07~09)과 올해 같은 석 달(2026.07~09) — 같은 단지·같은 84㎡대끼리만
print('\n[같은 단지 84㎡대: 2025.07~09 가운데 값 → 2026.07~09 가운데 값]')
A, B = rows(['202507', '202508', '202509']), rows(['202607', '202608', '202609'])
a = collections.defaultdict(list); b = collections.defaultdict(list)
for r in A:
    if r['umdNm'] == '상도동': a[r['aptNm']].append(num(r['dealAmount']))
for r in B:
    if r['umdNm'] == '상도동': b[r['aptNm']].append(num(r['dealAmount']))
ch = []
for k in sorted(set(a) & set(b)):
    if len(a[k]) >= 2 and len(b[k]) >= 2:
        x, y = st.median(a[k]), st.median(b[k]); ch.append((y / x - 1) * 100)
        print(f'  {k:16} {x/1e4:.2f}억({len(a[k])}건) → {y/1e4:.2f}억({len(b[k])}건) {(y/x-1)*100:+.1f}%')
if ch: print(f'  단지 {len(ch)}곳 변화율 가운데 값 {st.median(ch):+.1f}%')
print('  상도동 전체 84㎡대 건수', sum(len(v) for v in a.values()), '→', sum(len(v) for v in b.values()))
