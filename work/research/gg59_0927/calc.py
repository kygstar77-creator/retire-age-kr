# 경기도 전용 57~60.5㎡ 아파트 매매 실거래 중앙값(시 단위). 시 이름은 코드표를 베끼지 않고
# 거래 자료의 중개사 소재지(estateAgentSggNm) 최빈값으로 붙인다(구가 있는 시는 시로 묶는다).
import json, glob, os, statistics, sys, collections, re
sys.stdout.reconfigure(encoding='utf-8')
RT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rt')
by_code = collections.defaultdict(list); names = collections.defaultdict(collections.Counter); seen = set()
for f in glob.glob(os.path.join(RT, '41*_20260[789]_trade.json')):
    code = os.path.basename(f)[:5]
    for r in json.load(open(f, encoding='utf-8')):
        nm = (r.get('estateAgentSggNm') or '').strip()
        if nm.startswith('경기'): names[code][nm.split(',')[0]] += 1
        if r.get('cdealType'): continue
        a = float(r['excluUseAr'])
        if not (57 <= a <= 60.5): continue
        k = (r['aptSeq'], r['dealYear'], r['dealMonth'], r['dealDay'], r['floor'], r['dealAmount'], r['excluUseAr'])
        if k in seen: continue
        seen.add(k); by_code[code].append(int(r['dealAmount'].replace(',', '')))
city = collections.defaultdict(list); label = {}
for code, v in by_code.items():
    top = names[code].most_common(1)[0][0] if names[code] else code
    c = top.split()[1] if len(top.split()) > 1 else top
    c = re.sub(r'(수원|성남|안양|부천|안산|고양|용인|화성)시.*', r'\1시', c)
    c = re.sub(r'^(수원|성남|안양|부천|안산|고양|용인|화성)(?!시).*', r'\1시', c)
    label[code] = c; city[c] += v
res = sorted(((c, statistics.median(v), len(v)) for c, v in city.items() if len(v) >= 15), key=lambda x: -x[1])
print('경기 전용 57~60.5㎡, 2026-07~09 계약, 해제 제외, 중복 제거. 총', sum(len(v) for v in city.values()), '건 · 15건 미만 시군 제외')
for c, m, n in res: print('%s 중앙값 %.0f만원 (%d건)' % (c, m, n))
print('코드→이름:', dict(sorted(label.items())))
