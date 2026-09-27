# 인천 전용 57~60.5㎡·83~86㎡ 아파트 매매 실거래 구별 중앙값(2026-07~09 계약, 해제 제외, 중복 제거).
# 구 이름은 research/incheon_sgg.json(2026-07-01 행정체제 개편 뒤 코드: 제물포·영종·서해·검단 — 거래 자료의 동 이름으로 대조함).
import json, glob, os, statistics, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sgg = json.load(open(os.path.join(W, 'incheon_sgg.json'), encoding='utf-8'))
for lo, hi, lab in ((57, 60.5, '59㎡'), (83, 86, '84㎡')):
    by = collections.defaultdict(list); seen = set(); months = collections.Counter()
    for code, name in sgg.items():
        for f in glob.glob(os.path.join(W, 'rt', f'{code}_20260[789]_trade.json')):
            for r in json.load(open(f, encoding='utf-8')):
                if r.get('cdealType') or r.get('buyerGbn') == '공공기관': continue
                a = float(r['excluUseAr'])
                if not (lo <= a <= hi): continue
                k = (r['aptSeq'], r['dealYear'], r['dealMonth'], r['dealDay'], r['floor'], r['dealAmount'], r['excluUseAr'])
                if k in seen: continue
                seen.add(k); by[name].append(int(r['dealAmount'].replace(',', ''))); months[r['dealMonth']] += 1
    tot = sum(len(v) for v in by.values()); allv = [x for v in by.values() for x in v]
    print(f'\n[{lab}] 총 {tot}건 · 인천 전체 중앙값 {statistics.median(allv):.0f}만원 · 월별 {dict(months)}')
    for n, v in sorted(by.items(), key=lambda x: -statistics.median(x[1])):
        print(f'{n} 중앙값 {statistics.median(v):.0f}만원 ({len(v)}건) · 최저 {min(v)} 최고 {max(v)} · 비중 {len(v)/tot*100:.1f}%')
