# 오피스텔 월세 수익률(B10 지표 ⑤) — 국토부 실거래(work/research/rt/*_offi_*.json)로 구별·단지별 숫자만 낸다.
#   python work/offiyield.py 202607 202609
#   수익률 = 월세 × 12 ÷ (매매 중앙값 − 보증금). 같은 구·같은 단지·같은 5㎡ 면적대에서 매매 2건 이상·월세 2건 이상인 짝만.
import sys, os, re, json, glob, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'research', 'rt')
sgg = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
ym0, ym1 = sys.argv[1], sys.argv[2]
def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
def band(a):
    try: a = float(a)
    except (TypeError, ValueError): return None
    return int(a // 5 * 5)

def load(lawd, kind):
    rows = []
    for f in glob.glob(os.path.join(RT, f'{lawd}_*_offi_{kind}.json')):
        if ym0 <= os.path.basename(f).split('_')[1] <= ym1: rows += json.load(open(f, encoding='utf-8'))
    return rows

report, detail = [], []
for lawd, name in sgg.items():
    tr, rt = load(lawd, 'trade'), load(lawd, 'rent')
    sale = collections.defaultdict(list); wolse = collections.defaultdict(list)
    for r in tr:
        k = (r.get('offiNm', '').strip(), band(r.get('excluUseAr')))
        if not k[0] or k[1] is None or r.get('cdealType'): continue
        if num(r.get('dealAmount')) > 0: sale[k].append(num(r.get('dealAmount')))
    for r in rt:
        k = (r.get('offiNm', '').strip(), band(r.get('excluUseAr')))
        if not k[0] or k[1] is None: continue
        dep, mon = num(r.get('deposit')), num(r.get('monthlyRent'))
        if mon > 0: wolse[k].append((dep, mon))
    ys_all = []
    for k in sale:
        if len(sale[k]) >= 2 and len(wolse.get(k, [])) >= 2:
            p = statistics.median(sale[k])
            # 보증금이 매매가의 절반을 넘으면 준전세에 가까워 분모가 작아지고 수익률이 부풀려진다(2026-09-23 확인) — 뺀다
            used = [(d, m) for d, m in wolse[k] if p - d > 0 and d <= p * 0.5]
            if len(used) < 2: continue                   # 거른 뒤에도 월세 2건 이상이어야 한다
            ys = [(m * 12) / (p - d) for d, m in used]
            y = statistics.median(ys)
            if not (0.005 < y < 0.20): continue
            ys_all.append(y)
            # 표에 적는 보증금·월세 중앙값은 '수익률 계산에 실제로 쓴 계약'만으로 낸다(표와 수익률이 어긋나지 않게)
            dd = statistics.median([d for d, _ in used]); dm = statistics.median([m for _, m in used])
            detail.append((name, k[0], k[1], p, dd, dm, y, len(sale[k]), len(used)))
    if ys_all: report.append((name, len(tr), len(rt), len(ys_all), statistics.median(ys_all)))

report.sort(key=lambda x: -x[4])
print(f'서울 오피스텔 월세 수익률 ({ym0}~{ym1} 실거래, 같은 단지·같은 5㎡ 면적대에서 매매 2건·월세 2건 이상인 짝만)')
print('구 | 매매 건수 | 월세·전세 건수 | 짝 수 | 수익률 중앙값')
for name, nt, nr, n, med in report: print(f'{name} | {nt:,} | {nr:,} | {n} | {med*100:.2f}%')
detail.sort(key=lambda d: -d[6])
print('\n수익률 높은 단지·면적대 12')
for d in detail[:12]:
    print(f'  {d[0]} {d[1]} {d[2]}㎡대 | 매매 중앙 {d[3]/10000:.2f}억 · 보증금 중앙 {d[4]:,}만 · 월세 중앙 {d[5]:,}만 | {d[6]*100:.2f}% (매매 {d[7]}·월세 {d[8]}건)')
json.dump({'period': [ym0, ym1],
           'districts': [dict(zip(('name','trades','rents','pairs','yield'), r)) for r in report],
           'pairs': [dict(zip(('gu','offi','band','sale','deposit','rent','yield','n_sale','n_wolse'), d)) for d in detail]},
          open(os.path.join(RT, f'offiyield_{ym0}_{ym1}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
