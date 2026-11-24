# NDG-1 대조군·대칭 비교 (youtube-loop 2026-11-24, editor 반론 ①·②-2 답)
# ① 대칭: 같은 묶음의 '2021년 가운데 값' 대비 '2026-07~11 가운데 값'(꼭대기 한 건 대신)
# ② 대조군: 같은 셈을 서울 25개 구 전부에 — 노도강 90%가 서울 안에서 낮은 쪽인지
# 재료: work/research/rt/<구>_<월>_trade.json(국토부 아파트 매매) · 해제·공공기관 매수 뺌 · calc.py와 같은 묶음 규칙(동·단지·전용㎡ 반올림, 2026-07~11 3건 이상)
import json, os, glob, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
RT = os.path.join(W, 'rt'); sgg = json.load(open(os.path.join(W, 'seoul_sgg.json'), encoding='utf-8'))
NDG = {'11350', '11320', '11305'}
def num(s): return float(str(s or '0').replace(',', '') or 0) / 10000
def load(code):
    out = []
    for p in sorted(glob.glob(os.path.join(RT, f'{code}_*_trade.json'))):
        if 'offi' in p: continue
        ym = os.path.basename(p).split('_')[1]
        if not ('202101' <= ym <= '202611'): continue
        for r in json.load(open(p, encoding='utf-8')):
            if not isinstance(r, dict) or 'aptNm' not in r: continue
            if r.get('cdealType') or r.get('buyerGbn') == '공공기관': continue
            out.append((r.get('umdNm'), (r.get('aptNm') or '').strip(), round(float(r['excluUseAr'])),
                        f"{r['dealYear']}{str(r['dealMonth']).zfill(2)}", num(r['dealAmount'])))
    return out
def ratios(rows):
    g = collections.defaultdict(list)
    for d, a, ar, ym, amt in rows: g[(d, a, ar)].append((ym, amt))
    mx, md = [], []
    for v in g.values():
        p21 = [x for ym, x in v if ym[:4] == '2021']; now = [x for ym, x in v if '202607' <= ym <= '202611']
        if p21 and len(now) >= 3:
            mx.append(st.median(now) / max(p21)); md.append(st.median(now) / st.median(p21))
    return mx, md
allmx, allmd, ndgmx, ndgmd, othmx, othmd, per = [], [], [], [], [], [], []
for code, name in sgg.items():
    rows = load(code)
    months = {r[3] for r in rows}
    if len([m for m in months if m[:4] == '2021']) < 12 or len(months) < 70: print(f'{name}: 달 모자람(2021 {len([m for m in months if m[:4]=="2021"])}달·전체 {len(months)}달) — 뺌'); continue
    mx, md = ratios(rows)
    if not mx: continue
    per.append((st.median(mx), name, len(mx), st.median(md)))
    allmx += mx; allmd += md
    if code in NDG: ndgmx += mx; ndgmd += md
    else: othmx += mx; othmd += md
print(f'# 서울 {len(per)}개 구 · 묶음 {len(allmx)}')
print(f'서울 전체: 꼭대기 대비 가운데 {st.median(allmx)*100:.1f}% · 2021 가운데 대비 {st.median(allmd)*100:.1f}% · 꼭대기 넘은 묶음 {sum(1 for x in allmx if x>=1)}({sum(1 for x in allmx if x>=1)/len(allmx)*100:.0f}%)')
print(f'노도강: 꼭대기 대비 {st.median(ndgmx)*100:.1f}% · 2021 가운데 대비 {st.median(ndgmd)*100:.1f}% · 묶음 {len(ndgmx)}')
if othmx: print(f'노도강 뺀 서울: 꼭대기 대비 {st.median(othmx)*100:.1f}% · 2021 가운데 대비 {st.median(othmd)*100:.1f}% · 묶음 {len(othmx)} · 꼭대기 넘은 {sum(1 for x in othmx if x>=1)/len(othmx)*100:.0f}%')
print('\n## 구별 (꼭대기 대비 가운데 낮은 순) · 묶음 수 · 2021 가운데 대비')
for i, (m, name, n, mdd) in enumerate(sorted(per), 1): print(f'{i:2d}. {name} {m*100:.1f}% · {n}묶음 · {mdd*100:.1f}%')
