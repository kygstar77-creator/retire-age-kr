# 적정가 — 조건을 맞춰 견주고, 지금이 비싼지 싼지 숫자로 답한다.
#
#   py -3.12 work/fairprice.py 노원구              → 그 구에서 기준선 대비 싼 단지 순위
#   py -3.12 work/fairprice.py 노원구 상계주공9단지  → 그 단지의 평형·층별 적정가와 지금 위치
#
# 사장님 2026-09-25: "주식 부동산 둘 다 얼마가 적정가인지도, 지금 비싼지 싼지도 찾아줘야지.
#   부동산은 평수와 층과 위치와 여러 요소들이 너무 많잖아. 이런 걸 정리해 주고
#   비슷한 선상에서 비교해 주고 찾아주고 해야지. 다른 사람들은 손품 파는 게 귀찮으니까
#   우리가 여러 요소들을 분석해서 알려주는 거잖아."
#
# 무엇이 '적정가'인가 — 예측이 아니라 **같은 조건의 실제 거래 중앙값**이다.
#   같은 동 · 같은 5㎡ 면적대 · 같은 연식대(5년) · 같은 층대(저/중/고)로 묶어 중앙값을 낸다.
#   그 값이 기준선이고, 개별 거래가 기준선에서 얼마나 떨어져 있는지가 싸고 비싼 정도다.
#   "오른다·내린다"는 쓰지 않는다. 지금 위치만 숫자로 보여 주고 판단은 독자가 한다.
#
# 왜 조건을 맞추나 — 안 맞추면 숫자가 통째로 거짓이 된다(2026-09-23 실측):
#   아무것도 안 맞추면 광진 -36.8% · 면적만 맞추면 양천 -25.1% · 단지와 면적을 맞추면 양천 +2.6%.
import sys, os, re, json, glob, time, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.join(HERE, 'research', 'rt')
OUT = os.path.join(HERE, 'research', 'fairprice')

def num(x):
    try: return float(re.sub(r'[^\d.]', '', str(x) or '0') or 0)
    except Exception: return 0.0

try: SGG = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
except Exception: SGG = {}

def floor_band(f):
    """층은 같은 단지 안에서도 값을 가른다. 저·중·고 셋으로만 묶는다 —
    층마다 나누면 표본이 한두 건으로 쪼개져 중앙값이 뜻을 잃는다."""
    f = int(num(f))
    if f <= 0: return None
    return '저층(1~4층)' if f <= 4 else ('중층(5~12층)' if f <= 12 else '고층(13층~)')

def age_band(y):
    y = int(num(y))
    if y <= 0: return None
    age = time.localtime().tm_year - y
    for lo, hi, nm in ((0, 5, '5년 이내'), (5, 10, '5~10년'), (10, 20, '10~20년'), (20, 30, '20~30년')):
        if lo <= age < hi: return nm
    return '30년 이상'

def load(sgg_name=None, offi=False):
    """실거래를 읽어 한 건씩 펴 놓는다. 평당가·층대·연식대까지 붙인다."""
    rows = []
    for f in glob.glob(os.path.join(RT, '*_trade.json')):
        if ('_offi_' in os.path.basename(f)) != offi: continue
        try: data = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        for r in data:
            g = (r.get('sggNm') or SGG.get(str(r.get('sggCd', '')).strip()) or '').strip()
            if sgg_name and g != sgg_name: continue
            ar = num(r.get('excluUseAr')); amt = num(r.get('dealAmount'))
            nm = ((r.get('offiNm') if offi else r.get('aptNm')) or '').strip()
            fb = floor_band(r.get('floor')); ab = age_band(r.get('buildYear'))
            if not (g and nm and ar > 0 and amt > 0 and fb and ab): continue
            rows.append({'구': g, '동': (r.get('umdNm') or '').strip(), '단지': nm,
                         '면적': ar, '면적대': int(ar // 5 * 5), '평당가': amt / (ar / 3.3058),
                         '금액': amt, '층': int(num(r.get('floor'))), '층대': fb,
                         '연식대': ab, '준공': int(num(r.get('buildYear'))),
                         '월': f"{r.get('dealYear')}-{int(num(r.get('dealMonth'))):02d}"})
    return rows

MIN_N = 5      # 이보다 적으면 중앙값을 기준선으로 쓰지 않는다

def baselines(rows, keys):
    """주어진 조건으로 묶어 평당가 중앙값(기준선)을 낸다. 표본이 MIN_N 미만인 묶음은 버린다."""
    g = collections.defaultdict(list)
    for r in rows: g[tuple(r[k] for k in keys)].append(r['평당가'])
    return {k: statistics.median(v) for k, v in g.items() if len(v) >= MIN_N}, \
           {k: len(v) for k, v in g.items()}

def cheap_complexes(rows, top=12):
    """같은 동·같은 면적대·같은 연식대·같은 층대에서 기준선보다 싼 단지.
    조건을 맞췄으니 '싸다'가 입지나 평수 차이 때문이 아니다."""
    KEYS = ['동', '면적대', '연식대', '층대']
    base, n = baselines(rows, KEYS)
    per = collections.defaultdict(list)
    for r in rows:
        k = tuple(r[x] for x in KEYS)
        if k not in base: continue
        per[(r['구'], r['동'], r['단지'], r['면적대'], r['연식대'], r['층대'])].append(
            (r['평당가'] - base[k]) / base[k] * 100)
    out = []
    for key, gaps in per.items():
        if len(gaps) < 3: continue                       # 단지 쪽도 3건은 있어야 한다
        out.append({'구': key[0], '동': key[1], '단지': key[2], '면적대': key[3],
                    '연식대': key[4], '층대': key[5], '차이': statistics.median(gaps),
                    '건수': len(gaps),
                    '기준선': base[(key[1], key[3], key[4], key[5])],
                    '표본': n[(key[1], key[3], key[4], key[5])]})
    return sorted(out, key=lambda x: x['차이'])[:top]

def norm_name(t):
    """단지 이름을 맞춘다. 같은 단지인데 자료마다 이름이 다르다 —
    네이버 부동산은 '상계주공9단지', 국토부 실거래는 '상계주공9(고층)'이다(2026-09-25 확인).
    괄호 안 표기·'단지'·공백·중점을 떼고 견준다."""
    t = re.sub(r'[(（][^)）]*[)）]', '', str(t or ''))
    return re.sub(r'[\s·\-]|단지|아파트', '', t)

def complex_detail(rows, name):
    """한 단지의 평형·층별 적정가와 지금 위치."""
    key = norm_name(name)
    mine = [r for r in rows if key and key in norm_name(r['단지'])]
    if not mine:   # 반대 방향도 본다('상계주공9' 로 찾을 때 '상계주공9단지' 가 자료에 있는 경우)
        mine = [r for r in rows if key and norm_name(r['단지']) in key]
    if not mine: return None, []
    dong = collections.Counter(r['동'] for r in mine).most_common(1)[0][0]
    KEYS = ['동', '면적대', '연식대', '층대']
    base, _ = baselines(rows, KEYS)
    tbl = []
    for key, g in sorted(collections.defaultdict(list, {
            (r['면적대'], r['층대']): None for r in mine}).items()):
        sel = [r for r in mine if (r['면적대'], r['층대']) == key]
        if len(sel) < 2: continue
        med = statistics.median(r['평당가'] for r in sel)
        amt = statistics.median(r['금액'] for r in sel)
        b = base.get((dong, key[0], sel[0]['연식대'], key[1]))
        tbl.append({'면적대': key[0], '층대': key[1], '건수': len(sel),
                    '평당가': med, '실거래 중앙': amt, '동 기준선': b,
                    '차이': ((med - b) / b * 100) if b else None})
    return mine[0], tbl

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    offi = '--offi' in sys.argv
    if not args: sys.exit('구 이름을 주세요: py -3.12 work/fairprice.py 노원구 [단지이름] [--offi]')
    sgg = args[0]
    rows = load(sgg, offi)
    what = '오피스텔' if offi else '아파트'
    if not rows: sys.exit(f'{sgg} {what} 실거래가 없다 — work/research/rt/ 를 먼저 채운다(rtmolit.py)')
    print(f'[{sgg} {what}] 실거래 {len(rows)}건 · {rows[0]["월"]}~{max(r["월"] for r in rows)}')

    if len(args) > 1:
        r0, tbl = complex_detail(rows, args[1])
        if not r0: sys.exit(f'{args[1]} 거래가 없다')
        print(f'\n{r0["단지"]} ({r0["동"]} · {r0["준공"]}년 준공 · {r0["연식대"]})')
        print('  평형(전용)   층대          건수   평당가      실거래 중앙     같은 조건 기준선   차이')
        for t in tbl:
            b = f'{t["동 기준선"]:,.0f}만원' if t['동 기준선'] else '표본 부족'
            d = f'{t["차이"]:+.1f}%' if t['차이'] is not None else '—'
            print(f'  {t["면적대"]:>3}~{t["면적대"]+5:<3}㎡  {t["층대"]:<12} {t["건수"]:>3}건  '
                  f'{t["평당가"]:>7,.0f}만원  {t["실거래 중앙"]:>9,.0f}만원  {b:>12}  {d:>7}')
        print('\n  기준선 = 같은 동·같은 면적대·같은 연식대·같은 층대의 실거래 평당가 중앙값')
        print('  차이가 마이너스면 같은 조건 평균보다 싸게 거래됐다는 뜻이다. 오른다·내린다는 말이 아니다.')
        return

    cheap = cheap_complexes(rows)
    if not cheap: sys.exit('조건을 맞춘 묶음이 모자라 견줄 수 없다(표본 부족)')
    print(f'\n같은 동·같은 면적대·같은 연식대·같은 층대에서 **기준선보다 싼** 단지')
    print('  단지                    동         평형      연식      층대        차이     건수  기준선')
    for c in cheap:
        print(f'  {c["단지"][:20]:<20}  {c["동"][:8]:<8}  {c["면적대"]:>3}~{c["면적대"]+5:<3}㎡  '
              f'{c["연식대"]:<8}  {c["층대"]:<11}  {c["차이"]:+6.1f}%  {c["건수"]:>3}건  {c["기준선"]:,.0f}만원')
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f'{sgg}_{"offi" if offi else "apt"}_{time.strftime("%Y-%m-%d")}.json')
    json.dump(cheap, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\n  저장 {p}')
    print('  차이는 같은 조건 기준선 대비다. 싸게 거래된 데에는 우리가 못 본 이유가 있을 수 있다 —')
    print('  향·동간 거리·수리 상태는 실거래 자료에 없다. 글에 쓸 때 그 한계를 같이 적는다.')

if __name__ == '__main__': main()
