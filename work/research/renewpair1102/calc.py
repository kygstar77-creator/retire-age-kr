# 2026-11-02 firemap-write: h2s_renew 짝 글 — 갱신요구권 쓴 갱신 vs 안 쓴 갱신, 보증금 몇 % 올렸나
# 재료: raw/<구코드>_<월>_rent.json (국토부 아파트 전월세 실거래, 2026-11-02 21시 다시 받음, fetch.py)
# 거르기는 H-2 calc2.py와 같다: 14단지 · 전용 80~85㎡ · 월세 0(순수전세) · contractType 갱신 · 이전 보증금 있음
import json, os, sys, glob, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
FOCUS = {'잠실동': ['주공아파트5단지', '리센츠', '잠실엘스', '트리지움', '우성아파트'],
         '대치동': ['은마', '래미안대치팰리스', '대치르엘', '한보미도맨션1'],
         '반포동': ['래미안원베일리', '아크로리버파크', '래미안퍼스티지', '반포자이', '반포미도']}
def num(s): return float(str(s or '0').replace(',', '') or 0)
rows = []
for p in glob.glob(os.path.join(HERE, 'raw', '*_rent.json')):
    rows += [r for r in json.load(open(p, encoding='utf-8')) if isinstance(r, dict) and 'aptNm' in r]
def ok(r):
    a = r['aptNm'].replace(' ', '')
    return r['umdNm'] in FOCUS and a in FOCUS[r['umdNm']] and 80 <= num(r['excluUseAr']) < 85 and num(r['monthlyRent']) == 0
R = [r for r in rows if ok(r)]
ym = sorted({f"{r['dealYear']}{int(r['dealMonth']):02d}" for r in R})
print(f'# 기간 {ym[0]}~{ym[-1]} · 14단지 84㎡대 순수전세 {len(R)}건 (계약일 기준, 신고 30일 기한이라 10월은 늘 수 있음)')
ren = [r for r in R if r.get('contractType') == '갱신' and num(r.get('preDeposit')) > 0]
def rate(r): return (num(r['deposit']) / num(r['preDeposit']) - 1) * 100
used = [r for r in ren if r.get('useRRRight') == '사용']; nou = [r for r in ren if r.get('useRRRight') != '사용']
for name, g in (('갱신요구권 씀', used), ('안 씀(표시 없음)', nou)):
    x = [rate(r) for r in g]
    over = sum(v > 5.0001 for v in x); five = sum(4.95 <= v <= 5.0001 for v in x); same = sum(abs(v) < 0.01 for v in x); down = sum(v < -0.01 for v in x)
    print(f'- {name}: {len(g)}건 · 올린 폭 가운데 {st.median(x):.2f}% · 딱 5%(4.95~5) {five}건({five/len(g)*100:.0f}%) · 5% 넘김 {over}건({over/len(g)*100:.0f}%) · 그대로 {same} · 내림 {down} · 최대 {max(x):.1f}%')
    if name.startswith('안'):
        ov = sorted(v for v in x if v > 5.0001); print(f'  5% 넘긴 {len(ov)}건 올린 폭 가운데 {st.median(ov):.1f}%')
        amt = [num(r['deposit']) - num(r['preDeposit']) for r in g if rate(r) > 5.0001]; print(f'  5% 넘긴 계약 올린 금액 가운데 {st.median(amt):,.0f}만원')
    amtu = [num(r['deposit']) - num(r['preDeposit']) for r in g]; print(f'  올린 금액 가운데 {st.median(amtu):,.0f}만원 · 이전 보증금 가운데 {st.median([num(r["preDeposit"]) for r in g]):,.0f}만원')
print('\n## 단지별(갱신 10건 이상)')
for u, apts in FOCUS.items():
    for a in apts:
        g = [r for r in ren if r['umdNm'] == u and r['aptNm'].replace(' ', '') == a]
        if len(g) < 10: continue
        gu = [r for r in g if r.get('useRRRight') == '사용']; gn = [r for r in g if r.get('useRRRight') != '사용']
        print(f"- {a}: 갱신 {len(g)} · 씀 {len(gu)}(5% 넘김 {sum(rate(r) > 5.0001 for r in gu)}) · 안 씀 {len(gn)}(5% 넘김 {sum(rate(r) > 5.0001 for r in gn)}, 가운데 {st.median([rate(r) for r in gn]) if gn else 0:.1f}%)")
print('\n## 원베일리 84㎡대 신규 vs 갱신 가운데 값')
w = [r for r in R if r['aptNm'].replace(' ', '') == '래미안원베일리']
for t in ('신규', '갱신'):
    g = [num(r['deposit']) for r in w if r.get('contractType') == t]
    if g: print(f'- {t} {len(g)}건 가운데 {st.median(g):,.0f}만원')
print('\n## 예: 이전 보증금 10억이면 5% = 5,000만원')
