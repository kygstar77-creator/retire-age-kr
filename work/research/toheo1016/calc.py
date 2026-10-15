# 토허 신청(서울시 보도자료 10/15) 대 국토부 실거래 계약(조회 10/15) — 권역·월별
import json, glob, os, sys, collections, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
R = {'강남3구·용산': '서초 강남 송파 용산', '한강벨트': '광진 성동 마포 동작 양천 영등포 강동',
     '강북권': '종로 중 강북 노원 도봉 동대문 성북 중랑 서대문 은평', '서남권': '강서 관악 구로 금천'}
g2r = {}
for r, gs in R.items():
    for g in gs.split(): g2r[g + '구'] = r
APP = {'강남3구·용산': [1615, 1003, 687, 538, 355, 538], '한강벨트': [2058, 1433, 1162, 1023, 602, 778],
       '강북권': [3622, 2496, 2439, 2144, 1457, 1646], '서남권': [1601, 1079, 989, 913, 549, 716]}
MS = ['202604', '202605', '202606', '202607', '202608', '202609']
cnt = collections.Counter(); cancel = collections.Counter(); price = collections.defaultdict(list); bygu = collections.Counter()
for lawd, name in sgg.items():
    reg = g2r[name]
    for f in glob.glob(os.path.join(H, 'raw', f'{lawd}_*.json')):
        for r in json.load(open(f, encoding='utf-8')):
            ym = r['dealYear'] + r['dealMonth'].zfill(2)
            if ym not in MS: continue
            if r.get('cdealType'): cancel[(reg, ym)] += 1; continue
            cnt[(reg, ym)] += 1; bygu[(name, ym)] += 1
            a = float(r['excluUseAr']); p = float(r['dealAmount'].replace(',', ''))
            if 59 <= a < 60.5 or 84 <= a < 85.5: price[(reg, ym)].append(p / (a / 3.305785))
print('권역 | 월 | 허가신청 | 실거래(해제 뺌) | 해제 | 실거래/신청 | 평당 중앙(만원,59·84㎡)')
tot = collections.Counter()
for r in R:
    for i, m in enumerate(MS):
        a = APP[r][i]; c = cnt[(r, m)]; tot[(m, 'a')] += a; tot[(m, 'c')] += c
        pr = int(st.median(price[(r, m)])) if price[(r, m)] else 0
        print(f'{r} | {m} | {a:,} | {c:,} | {cancel[(r,m)]} | {c/a*100:.1f}% | {pr:,}')
print('서울 합계')
for m in MS:
    print(f'{m} 신청 {tot[(m,"a")]:,} 실거래 {tot[(m,"c")]:,} 비율 {tot[(m,"c")]/tot[(m,"a")]*100:.1f}%')
# 다음 달 실거래 / 이번 달 신청 (허가 뒤 계약이라 한 달 밀림)
print('실거래(다음 달)/신청(이번 달)')
for i in range(5):
    print(MS[i], '→', MS[i+1], f'{tot[(MS[i+1],"c")]/tot[(MS[i],"a")]*100:.1f}%')
json.dump({f'{k[0]}|{k[1]}': v for k, v in bygu.items()}, open(os.path.join(H, 'bygu.json'), 'w', encoding='utf-8'), ensure_ascii=False)
