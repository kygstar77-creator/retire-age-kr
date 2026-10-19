# h1walkcafe1020 — h1s_walk(고덕동 역 180m vs 640m) 짝 글 계산. 국토부 실거래(research/rt/11740_*, 2026-10-20 07:4x 다시 받음) + tour.py 결과(raw/tour_godeok_1020.json).
import sys, os, json, glob, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(H, '..', 'rt')
T = json.load(open(os.path.join(H, 'raw', 'tour_godeok_1020.json'), encoding='utf-8'))
OLD = json.load(open(os.path.join(H, '..', 'longform', 'ep', 'H-1', 'raw', 'tour_godeok.json'), encoding='utf-8'))
ms = sorted({os.path.basename(f).split('_')[1] for f in glob.glob(os.path.join(RT, '11740_2*_trade.json'))})[-12:]
rows = []
for m in ms:
    d = json.load(open(os.path.join(RT, f'11740_{m}_trade.json'), encoding='utf-8')); rows += d if isinstance(d, list) else d.get('rows', [])
rows = [r for r in rows if r.get('umdNm') == '고덕동' and not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
print('월', ms[0], '~', ms[-1], '고덕동 매매(해제·공공 뺌)', len(rows))
num = lambda s: float(str(s).replace(',', '') or 0)
def key(n): return n.replace(' ', '')
name_map = {}
for c in T['complexes']:
    name_map[c['name']] = c
# 실거래 단지명 → tour 단지명(공백·순서 무시 근사)
def match(apt):
    a = key(apt)
    for n in name_map:
        k = key(n)
        if a == k or set(a) == set(k) and len(a) == len(k): return n
    for n in name_map:
        if key(n) in a or a in key(n): return n
    return None
by = {}
for r in rows:
    n = match(r['aptNm'])
    if not n: continue
    ar = num(r['excluUseAr'])
    if 80 <= ar < 86:
        by.setdefault(n, []).append(r)
print('\n§1 단지별 84㎡대(전용 80~85㎡) 1년 매매 가운데 값 · 역까지 걷는 거리 순')
out = []
for n, c in sorted(name_map.items(), key=lambda x: x[1]['walk']['station']['m']):
    rs = by.get(n, [])
    amts = sorted(num(r['dealAmount']) for r in rs)
    med = st.median(amts) if amts else None
    ar = st.median(num(r['excluUseAr']) for r in rs) if rs else None
    k = c['kapt']; w = c['walk']['station']
    out.append(dict(name=n, use=k['use'], hh=k['hh'], st=w['name'], m=w['m'], n84=len(amts), med84=med, ppy=c['ppyTop'], area=ar, kaptWalk=k['subwayWalk'], kaptSub=k['subway']))
    print(f"{n} | 입주 {k['use']} · {k['hh']}세대 | {w['name']} {w['m']}m (관리사무소 등록 {k['subway']} {k['subwayWalk']}) | 84㎡대 {len(amts)}건 가운데 {med/10000 if med else None}억 · 평당 {c['ppyTop']}만원(tour, ±20% 밖 뺌) · 전용 가운데 {ar}")
g = {o['name']: o for o in out}
a, b = g['고덕 그라시움'], g['래미안힐스테이트 고덕']
print('\n§2 그라시움 vs 래미안힐스테이트 고덕')
print(' 평당', a['ppy'], b['ppy'], '차', round((a['ppy'] / b['ppy'] - 1) * 100, 1), '%')
print(' 한 채 가운데', a['med84'], b['med84'], '차', a['med84'] - b['med84'], '만원')
print(' 걸음 비', round(b['m'] / a['m'], 2))
print('\n§3 역 640~700m 네 곳끼리')
grp = [o for o in out if 600 <= o['m'] <= 700]
for o in grp: print(' ', o['name'], o['use'], o['m'], o['ppy'], o['n84'], o['med84'])
pp = [o['ppy'] for o in grp if o['ppy']]
print(' 평당 최고/최저', max(pp), min(pp), '차', round((max(pp) / min(pp) - 1) * 100, 1), '%')
f = g['고덕풍경채어바니티']
print('\n§4 가장 새 단지(2024) 풍경채어바니티 vs 래미안힐스테이트 고덕(2016)', f['m'], f['ppy'], b['ppy'], round((f['ppy'] / b['ppy'] - 1) * 100, 1), '%', '한 채', f['med84'], b['med84'])
# 늦게 신고된 거래: 10/11 받은 H-1 tour에 없던 84㎡대 거래
old_deals = {}
for c in OLD['complexes']:
    old_deals[c['name']] = c.get('nTop')
print('\n§5 10/11 받은 자료(H-1) 대비 84㎡대 건수')
for o in out:
    print(' ', o['name'], '10/11', old_deals.get(o['name']), '→ 10/20', o['n84'], '(tour 평당 건수)', [c['nTop'] for c in T['complexes'] if c['name'] == o['name']][0])
print('\n§6 9~10월 계약 84㎡대 거래(신고일 있는 것)')
for n in ('고덕 그라시움', '래미안힐스테이트 고덕'):
    for r in sorted(by.get(n, []), key=lambda r: (int(r['dealYear']), int(r['dealMonth']), int(r['dealDay']))):
        if int(r['dealYear']) == 2026 and int(r['dealMonth']) >= 9:
            print(' ', n, f"{r['dealYear']}-{int(r['dealMonth']):02d}-{int(r['dealDay']):02d}", r['dealAmount'], r['floor'] + '층', r['excluUseAr'], r.get('dealingGbn'), '등기', r.get('rgstDate'))
json.dump(out, open(os.path.join(H, 'calc_out.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
