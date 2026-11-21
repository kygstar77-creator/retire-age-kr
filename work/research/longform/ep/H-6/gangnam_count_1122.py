# H-6 지시(benchmark 11/22): 강남구 전체 아파트 매매 월별 신고 건수 vs 은마 — 국토부 실거래 11/22 다시 받음
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import rtmolit
OUT = os.path.join(os.path.dirname(__file__), 'raw', 'gangnam_1122'); os.makedirs(OUT, exist_ok=True)
yms = ['202510','202511','202512'] + [f'2026{m:02d}' for m in range(1, 12)]
tot = {}
for ym in yms:
    rows = rtmolit.fetch('trade', '11680', ym)
    json.dump(rows, open(os.path.join(OUT, f'{ym}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    live = [r for r in rows if not r.get('cdealType')]
    em = [r for r in live if '은마' in r.get('aptNm', '')]
    em84 = [r for r in em if 76 <= float(r.get('excluUseAr') or 0) <= 85]
    tot[ym] = (len(rows), len(live), len(em), len(em84))
    print(ym, '전체', len(rows), '해제 뺀', len(live), '은마', len(em), '은마77·84', len(em84))
y = [k for k in yms if '202511' <= k <= '202610']
a = sum(tot[k][1] for k in y); s = tot['202609'][1] + tot['202610'][1]
e = sum(tot[k][3] for k in y); es = tot['202609'][3] + tot['202610'][3]
print(f'강남구 2025.11~2026.10 해제 뺀 {a}건 · 9~10월 {s}건 = {s/a*100:.1f}% · 월 평균 {a/12:.0f}건 vs 9~10월 평균 {s/2:.0f}건')
print(f'은마(77·84) 같은 기간 {e}건 · 9~10월 {es}건 = {es/e*100:.1f}%')
