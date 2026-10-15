# 같은 단지·같은 면적대(59㎡대·84㎡대) 8월 대 9월 계약 평당가 — 권역별(국토부 실거래, 조회 2026-10-15, 해제 뺌)
import json, glob, os, sys, collections, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
R = {'강남3구·용산': '서초 강남 송파 용산', '한강벨트': '광진 성동 마포 동작 양천 영등포 강동',
     '강북권': '종로 중 강북 노원 도봉 동대문 성북 중랑 서대문 은평', '서남권': '강서 관악 구로 금천'}
g2r = {g + '구': r for r, gs in R.items() for g in gs.split()}
cell = collections.defaultdict(list)
for lawd, name in sgg.items():
    for m in ('202608', '202609'):
        for r in json.load(open(os.path.join(H, 'raw', f'{lawd}_{m}.json'), encoding='utf-8')):
            if r.get('cdealType'): continue
            a = float(r['excluUseAr'])
            band = '59' if 59 <= a < 60.5 else '84' if 84 <= a < 85.5 else None
            if not band: continue
            p = float(r['dealAmount'].replace(',', '')) / (a / 3.305785)
            cell[(g2r[name], name, r['aptSeq'] if r.get('aptSeq') else r['aptNm'], band, m)].append(p)
out = collections.defaultdict(list); n8 = collections.Counter(); n9 = collections.Counter()
keys = {k[:4] for k in cell}
for k in keys:
    a, b = cell.get(k + ('202608',)), cell.get(k + ('202609',))
    if a and b:
        out[k[0]].append(st.median(b) / st.median(a) - 1); n8[k[0]] += len(a); n9[k[0]] += len(b)
allc = []
print('권역 | 짝지은 칸 | 8월 건 | 9월 건 | 변화율 가운데 값 | 오른 칸 비율')
for r in R:
    v = out[r]; allc += v
    print(f'{r} | {len(v)} | {n8[r]} | {n9[r]} | {st.median(v)*100:+.2f}% | {sum(x>0 for x in v)/len(v)*100:.0f}%')
print(f'서울 | {len(allc)} | {sum(n8.values())} | {sum(n9.values())} | {st.median(allc)*100:+.2f}% | {sum(x>0 for x in allc)/len(allc)*100:.0f}%')
# 레드팀 1차(10/15 09:4x) 보강: 오름·내림·같음 비율과 평균
up = sum(x > 0 for x in allc); dn = sum(x < 0 for x in allc); eq = len(allc) - up - dn
print(f'오름 {up}({up/len(allc)*100:.1f}%) 내림 {dn}({dn/len(allc)*100:.1f}%) 같음 {eq}({eq/len(allc)*100:.1f}%) 평균 {st.mean(allc)*100:+.2f}%')
for r in R: print(r, f'평균 {st.mean(out[r])*100:+.2f}%')
