# H-3 계산 재현 — 숫자는 전부 여기서 나온다(대본·카페·쇼츠 공통). 실행: py -3.12 work/research/longform/ep/H-3/calc.py > calc_out.txt
# 재료: raw/rt/<구코드>_<월>_{trade,rent}.json = 국토교통부 아파트 매매·전월세 실거래(공공데이터포털 1613000, rtmolit.fetch로 2026-10-16 12:4x 새로 받음)
#       H-2가 쓰는 work/research/rt/ 파일은 건드리지 않으려고 H-3 폴더에 따로 받았다(9월 늦은 신고 반영).
# 네이버 부동산 등 민간 화면·호가·매물·경매·분담금 예상은 쓰지 않는다. 단지명은 국토부 aptNm 그대로.
import json, os, sys, re, glob, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
PY = 3.305785
def num(s): return float(str(s or '0').replace(',', '') or 0)
def eok(m): return f'{m/10000:.2f}억'
def load(lawd, kind):
    out = []
    for p in sorted(glob.glob(os.path.join(RT, f'{lawd}_*_{kind}.json'))): out += json.load(open(p, encoding='utf-8'))
    return out
def ok(r): return not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
def pp(r): return num(r['dealAmount']) / num(r['excluUseAr']) * PY
def ar(r): return num(r['excluUseAr'])
def ym(r): return f"{r['dealYear']}.{str(r['dealMonth']).zfill(2)}"
def med(v): return st.median(v) if v else 0
def line(tag, rs):
    if not rs: return f'{tag} 0건'
    p = [pp(r) for r in rs]; a = [num(r['dealAmount']) for r in rs]
    d = sum(1 for r in rs if r.get('dealingGbn') == '직거래')
    return f'{tag} {len(rs)}건 · 평당 중앙 {med(p):,.0f}만원(최저 {min(p):,.0f}·최고 {max(p):,.0f}) · 매매 중앙 {eok(med(a))}(최저 {eok(min(a))}·최고 {eok(max(a))}) · 직거래 {d}'

ALL = {'11470': load('11470', 'trade'), '11680': load('11680', 'trade'), '11710': load('11710', 'trade')}
print('# H-3 calc_out — 단위 만원, 평당 = 전용면적 기준 3.305785㎡. 해제·공공기관 매수 제외. 계약월 2025.11~2026.10(10월은 신고 기한 30일이라 덜 들어옴)\n')

print('## 0. 거래량 관문(최근 3개월 = 2026.07~10 계약, 매매 20건 미만 동네는 뺀다 — series-plan 9-1③)')
for lawd, umd in [('11680', '압구정동'), ('11710', '신천동'), ('11470', '목동'), ('11470', '신정동')]:
    t = [r for r in ALL[lawd] if r['umdNm'] == umd and ok(r)]
    rec = [r for r in t if (int(r['dealYear']), int(r['dealMonth'])) >= (2026, 7)]
    cx = sum(1 for r in ALL[lawd] if r['umdNm'] == umd and r.get('cdealType'))
    print(f'- {umd}: 1년 매매 {len(t)}건 · 7~10월 {len(rec)}건 · 해제 {cx}건(뺌) · 계약월 {min(map(ym, t))}~{max(map(ym, t))}')

print('\n## 1. 목동신시가지 1~14단지 — 번호와 법정동(국토부 umdNm), 단지별 1년')
MS = [r for r in ALL['11470'] if ok(r) and '목동신시가지' in r['aptNm']]
G = collections.defaultdict(list)
for r in MS: G[int(re.search(r'\d+', r['aptNm'].replace('목동신시가지', '')).group())].append(r)
for k in sorted(G):
    rs = G[k]; by = sorted({r.get('buildYear') for r in rs if r.get('buildYear')})
    band = [r for r in rs if 60 <= ar(r) < 70]
    print(f'- {k}단지 · {rs[0]["umdNm"]} · 준공 {"/".join(by) or "-"} · 면적 {sorted({round(ar(r)) for r in rs})}')
    print('  ' + line('전 면적', rs)); print('  ' + line('60~70㎡대', band))
mok = [r for k in range(1, 8) for r in G[k] if 60 <= ar(r) < 70]; sin = [r for k in range(8, 15) for r in G[k] if 60 <= ar(r) < 70]
print('- ' + line('목동 쪽(1~7단지) 60~70㎡대 모아서', mok)); print('- ' + line('신정동 쪽(8~14단지) 60~70㎡대 모아서', sin))
a, b = med([pp(r) for r in mok]), med([pp(r) for r in sin])
print(f'- 60~70㎡대 평당 중앙: 목동 쪽이 신정동 쪽보다 {a/b*100-100:+.1f}% ({a:,.0f} vs {b:,.0f})')
for x, y in [(7, 11), (1, 11), (3, 11)]:
    p1 = med([pp(r) for r in G[x] if 60 <= ar(r) < 70]); p2 = med([pp(r) for r in G[y] if 60 <= ar(r) < 70])
    if p1 and p2: print(f'  · {x}단지 vs {y}단지(60~70㎡대): {p1:,.0f} vs {p2:,.0f} → {p1/p2*100-100:+.1f}%')

print('\n## 2. 압구정동 — 단지별(번호 붙은 현대·신현대·한양·미성) 평당 중앙, 높은 순')
AP = [r for r in ALL['11680'] if ok(r) and r['umdNm'] == '압구정동']
G2 = collections.defaultdict(list)
for r in AP: G2[r['aptNm']].append(r)
for k, rs in sorted(G2.items(), key=lambda x: -med([pp(r) for r in x[1]])):
    print(f'- {k} · 준공 {rs[0].get("buildYear")} · 면적 {sorted({round(ar(r)) for r in rs})} · ' + line('', rs).strip())
print('\n### 2-1. 압구정동 면적대별(단지 섞어서) — 큰 집일수록 평당이 싼가')
for lo, hi in [(0, 90), (90, 130), (130, 170), (170, 999)]:
    print('- ' + line(f'{lo}~{hi}㎡', [r for r in AP if lo <= ar(r) < hi]))

print('\n## 3. 신천동 — 장미1·2·3(1979·1984)과 파크리오(2008), 같은 면적끼리')
SC = [r for r in ALL['11710'] if ok(r) and r['umdNm'] == '신천동']
for nm in ['장미1', '장미2', '장미3', '파크리오']:
    rs = [r for r in SC if r['aptNm'] == nm]
    print(f'- {nm} · 준공 {sorted({r.get("buildYear") for r in rs})} · ' + line('전 면적', rs).strip())
    for a0 in sorted({round(ar(r)) for r in rs}):
        print('  ' + line(f'{a0}㎡', [r for r in rs if round(ar(r)) == a0]))
j82 = [r for r in SC if r['aptNm'] in ('장미1', '장미2') and 80 <= ar(r) < 85]; p85 = [r for r in SC if r['aptNm'] == '파크리오' and 80 <= ar(r) < 86]
print('- ' + line('장미1·2 82㎡ 모아서', j82)); print('- ' + line('파크리오 84㎡대', p85))
print(f'- 82~84㎡대 평당: 장미1·2가 파크리오보다 {med([pp(r) for r in j82])/med([pp(r) for r in p85])*100-100:+.1f}%')

print('\n## 4. 세 동네 공통 — 같은 단지 안 작은 집 vs 큰 집 평당(거래 5건 이상 면적만)')
for tag, rs_all in [('파크리오', [r for r in SC if r['aptNm'] == '파크리오']), ('장미1', [r for r in SC if r['aptNm'] == '장미1']),
                    ('신현대12차', G2.get('신현대12차', [])), ('목동신시가지7', G[7]), ('목동신시가지3', G[3])]:
    c = collections.defaultdict(list)
    for r in rs_all: c[round(ar(r))].append(pp(r))
    c = {k: v for k, v in c.items() if len(v) >= 5}
    if len(c) >= 2:
        lo, hi = min(c), max(c)
        print(f'- {tag}: {lo}㎡ 평당 {med(c[lo]):,.0f}({len(c[lo])}건) vs {hi}㎡ 평당 {med(c[hi]):,.0f}({len(c[hi])}건) → 작은 집이 {med(c[lo])/med(c[hi])*100-100:+.1f}%')

print('\n## 5. 같은 돈이면 어디서 몇 ㎡ — 매매가 ±10% 안 거래의 전용면적 중앙(동네별)')
POOL = {'압구정동': AP, '신천동': SC, '목동(신시가지)': [r for k in range(1, 8) for r in G[k]], '신정동(신시가지)': [r for k in range(8, 15) for r in G[k]]}
for B in [200000, 300000, 400000]:
    parts = []
    for k, rs in POOL.items():
        m = [r for r in rs if B * 0.9 <= num(r['dealAmount']) <= B * 1.1]
        if m:
            top = collections.Counter(r['aptNm'] for r in m).most_common(2)
            parts.append(f'{k} {len(m)}건 전용 중앙 {med([ar(r) for r in m]):.0f}㎡({", ".join(f"{n} {c}" for n, c in top)})')
        else: parts.append(f'{k} 0건')
    print(f'- {eok(B)} 안팎: ' + ' / '.join(parts))
