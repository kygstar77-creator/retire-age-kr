# 저평가 지표 계산(B10) — 국토부 실거래(work/research/rt/*.json)로 구별·단지별 숫자만 낸다. '사라/사지 마라' 없음(사장님 규칙).
#   python work/undervalue.py 202607 202609             → 서울 25개 구 전세가율(전세 보증금 ÷ 매매가, 같은 단지·같은 면적대 실거래 짝) 표 + 단지별 상위/하위
#   python work/undervalue.py 202607 202609 research/gyeonggi_sgg.json 경기  → 다른 지역(코드→시·구 이름 표). 같은 이름 코드(수원 4개 구 등)는 한 줄로 묶는다(2026-09-27)
#   python work/undervalue.py 202607 202609 --min 2 --minarea 40  → 단지 순위(높은/낮은 10)에만 문턱: 매매·전세 각 N건 이상, 전용 40㎡대 이상(2026-10-02, 문턱 없으면 15㎡ 초소형 1~2건이 상위를 채움 — plans/sonpum.md 숫자 규칙)
#   지표: ① 전세가율 ② 월세 수익률(월세×12 ÷ (매매−보증금)) — 같은 단지·면적대 짝이 있을 때만
import sys, os, re, json, glob, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'research', 'rt')
def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default
MIN_N = int(opt('--min', 2))          # 단지 순위에 넣을 매매·전세 각 최소 건수(구 표는 늘 2건)
MIN_AREA = float(opt('--minarea', 0))  # 단지 순위 면적대 하한(㎡)
pos = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and sys.argv[i - 1] not in ('--min', '--minarea')]
ym0, ym1 = pos[0], pos[1]
SGGF = pos[2] if len(pos) > 2 else os.path.join(HERE, 'research', 'seoul_sgg.json')
REGION = pos[3] if len(pos) > 3 else '서울'
sgg = json.load(open(SGGF if os.path.isabs(SGGF) or os.path.exists(SGGF) else os.path.join(HERE, SGGF), encoding='utf-8'))
groups = collections.OrderedDict()
for lawd, name in sgg.items(): groups.setdefault(name, []).append(lawd)
def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
def band(a):
    try: a = float(a)
    except ValueError: return None
    return int(a // 5 * 5)   # 5㎡ 단위 면적대

def load(lawds, kind):
    rows = []
    for lawd in lawds:
        for f in glob.glob(os.path.join(RT, f'{lawd}_*_{kind}.json')):
            ym = os.path.basename(f).split('_')[1]
            if ym0 <= ym <= ym1: rows += json.load(open(f, encoding='utf-8'))
    return rows

report = []
detail = []
for name, lawds in groups.items():
    tr, rt = load(lawds, 'trade'), load(lawds, 'rent')
    sale = collections.defaultdict(list); jeonse = collections.defaultdict(list); wolse = collections.defaultdict(list)
    for r in tr:
        k = (r.get('aptNm', '').strip(), band(r.get('excluUseAr')), (r.get('umdNm') or '').strip())   # 법정동까지 — 같은 구 같은 이름 다른 단지(노원 '극동' 상계 1996·하계 1988)가 한 덩어리로 섞였다(2026-10-02 write)
        if not k[0]: continue   # 단지명이 빈 거래는 한 덩어리로 묶여 전세가율이 119%처럼 튄다(2026-09-23 확인) — 뺀다
        if k[1] is not None and num(r.get('dealAmount')) > 0 and not r.get('cdealType') and r.get('buyerGbn') != '공공기관': sale[k].append(num(r.get('dealAmount')))   # 만원, 해제거래·공공기관 일괄 매입 제외(2026-09-27)
    for r in rt:
        k = (r.get('aptNm', '').strip(), band(r.get('excluUseAr')), (r.get('umdNm') or '').strip())   # 법정동까지 — 같은 구 같은 이름 다른 단지(노원 '극동' 상계 1996·하계 1988)가 한 덩어리로 섞였다(2026-10-02 write)
        if not k[0]: continue
        if k[1] is None: continue
        dep, mon = num(r.get('deposit')), num(r.get('monthlyRent'))
        if mon == 0 and dep > 0: jeonse[k].append(dep)
        elif mon > 0: wolse[k].append((dep, mon))
    ratios, yields = [], []
    for k in sale:
        if len(sale[k]) >= 2 and len(jeonse.get(k, [])) >= 2:
            p, j = statistics.median(sale[k]), statistics.median(jeonse[k]); r_ = j / p
            if 0.2 < r_ < 1.2: ratios.append(r_); detail.append((name, k[0], k[1], p, j, r_, len(sale[k]), len(jeonse[k])))
        if len(sale[k]) >= 2 and len(wolse.get(k, [])) >= 2:
            p = statistics.median(sale[k]); ys = [(m * 12) / (p - d) for d, m in wolse[k] if p - d > 0]
            if ys: yields.append(statistics.median(ys))
    report.append((name, len(tr), len(rt), len(ratios), statistics.median(ratios) if ratios else None, statistics.median(yields) if yields else None))

report.sort(key=lambda x: -(x[4] or 0))
print(f'{REGION} {len(groups)}개 시·구 전세가율 ({ym0}~{ym1} 실거래, 같은 단지·같은 5㎡ 면적대에서 매매·전세 각 2건 이상인 짝만)')
print('구 | 매매 건수 | 전월세 건수 | 짝 수 | 전세가율 중앙값 | 월세 수익률 중앙값')
for name, nt, nr, npair, med, yl in report:
    print(f'{name} | {nt:,} | {nr:,} | {npair} | {med*100:.1f}% | ' + (f'{yl*100:.2f}%' if yl else '-') if med else f'{name} | {nt:,} | {nr:,} | {npair} | - | -')
detail.sort(key=lambda d: -d[5])
ranked = [d for d in detail if d[2] >= MIN_AREA and d[6] >= MIN_N and d[7] >= MIN_N]
cond = f'매매·전세 각 {MIN_N}건 이상' + (f'·전용 {MIN_AREA:g}㎡대 이상' if MIN_AREA else '')
print(f'\n전세가율 높은 단지·면적대 10 (전세가 매매가에 가장 가까움 · {cond}, {len(ranked)}개 중)')
for d in ranked[:10]: print(f'  {d[0]} {d[1]} {d[2]}㎡대 | 매매 중앙 {d[3]/10000:.1f}억 · 전세 중앙 {d[4]/10000:.1f}억 | 전세가율 {d[5]*100:.0f}% (매매 {d[6]}·전세 {d[7]}건)')
print(f'\n전세가율 낮은 단지·면적대 10 ({cond})')
for d in ranked[-10:]: print(f'  {d[0]} {d[1]} {d[2]}㎡대 | 매매 중앙 {d[3]/10000:.1f}억 · 전세 중앙 {d[4]/10000:.1f}억 | 전세가율 {d[5]*100:.0f}% (매매 {d[6]}·전세 {d[7]}건)')
json.dump({'period': [ym0, ym1], 'rank_filter': {'min': MIN_N, 'minarea': MIN_AREA, 'n': len(ranked)}, 'districts': [dict(zip(('name', 'trades', 'rents', 'pairs', 'jeonse_ratio', 'rent_yield'), r)) for r in report], 'pairs': [dict(zip(('gu', 'apt', 'band', 'sale', 'jeonse', 'ratio', 'n_sale', 'n_jeonse'), d)) for d in detail]}, open(os.path.join(HERE, 'research', 'rt', f'undervalue_{ym0}_{ym1}.json' if REGION == '서울' else f'undervalue_{REGION}_{ym0}_{ym1}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
