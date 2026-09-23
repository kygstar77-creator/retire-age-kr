# 저평가 지표 계산(B10) — 국토부 실거래(work/research/rt/*.json)로 구별·단지별 숫자만 낸다. '사라/사지 마라' 없음(사장님 규칙).
#   python work/undervalue.py 202607 202609             → 서울 25개 구 전세가율(전세 보증금 ÷ 매매가, 같은 단지·같은 면적대 실거래 짝) 표 + 단지별 상위/하위
#   지표: ① 전세가율 ② 월세 수익률(월세×12 ÷ (매매−보증금)) — 같은 단지·면적대 짝이 있을 때만
import sys, os, re, json, glob, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'research', 'rt')
sgg = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
ym0, ym1 = sys.argv[1], sys.argv[2]
def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
def band(a):
    try: a = float(a)
    except ValueError: return None
    return int(a // 5 * 5)   # 5㎡ 단위 면적대

def load(lawd, kind):
    rows = []
    for f in glob.glob(os.path.join(RT, f'{lawd}_*_{kind}.json')):
        ym = os.path.basename(f).split('_')[1]
        if ym0 <= ym <= ym1: rows += json.load(open(f, encoding='utf-8'))
    return rows

report = []
detail = []
for lawd, name in sgg.items():
    tr, rt = load(lawd, 'trade'), load(lawd, 'rent')
    sale = collections.defaultdict(list); jeonse = collections.defaultdict(list); wolse = collections.defaultdict(list)
    for r in tr:
        k = (r.get('aptNm', '').strip(), band(r.get('excluUseAr')))
        if k[1] is not None and num(r.get('dealAmount')) > 0 and not r.get('cdealType'): sale[k].append(num(r.get('dealAmount')))   # 만원, 해제거래 제외
    for r in rt:
        k = (r.get('aptNm', '').strip(), band(r.get('excluUseAr')))
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
print(f'서울 25개 구 전세가율 ({ym0}~{ym1} 실거래, 같은 단지·같은 5㎡ 면적대에서 매매·전세 각 2건 이상인 짝만)')
print('구 | 매매 건수 | 전월세 건수 | 짝 수 | 전세가율 중앙값 | 월세 수익률 중앙값')
for name, nt, nr, npair, med, yl in report:
    print(f'{name} | {nt:,} | {nr:,} | {npair} | {med*100:.1f}% | {yl*100:.2f}%' if med else f'{name} | {nt:,} | {nr:,} | {npair} | - | -')
detail.sort(key=lambda d: -d[5])
print('\n전세가율 높은 단지·면적대 10 (전세가 매매가에 가장 가까움)')
for d in detail[:10]: print(f'  {d[0]} {d[1]} {d[2]}㎡대 | 매매 중앙 {d[3]/10000:.1f}억 · 전세 중앙 {d[4]/10000:.1f}억 | 전세가율 {d[5]*100:.0f}% (매매 {d[6]}·전세 {d[7]}건)')
print('\n전세가율 낮은 단지·면적대 10')
for d in detail[-10:]: print(f'  {d[0]} {d[1]} {d[2]}㎡대 | 매매 중앙 {d[3]/10000:.1f}억 · 전세 중앙 {d[4]/10000:.1f}억 | 전세가율 {d[5]*100:.0f}% (매매 {d[6]}·전세 {d[7]}건)')
json.dump({'period': [ym0, ym1], 'districts': [dict(zip(('name', 'trades', 'rents', 'pairs', 'jeonse_ratio', 'rent_yield'), r)) for r in report], 'pairs': [dict(zip(('gu', 'apt', 'band', 'sale', 'jeonse', 'ratio', 'n_sale', 'n_jeonse'), d)) for d in detail]}, open(os.path.join(HERE, 'research', 'rt', f'undervalue_{ym0}_{ym1}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
