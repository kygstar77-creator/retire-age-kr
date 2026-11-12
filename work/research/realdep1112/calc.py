# realdep1112 (write-b 2026-11-12): k1s_dep 쇼츠 짝 글 — 1억 1년 정기예금 세후 이자, 물가 빼면 실제 얼마 남나
import sys, json, urllib.request, time
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
K = apis.key('ecos')
def ecos(stat, cyc, s, e, item):
    u = f'https://ecos.bok.or.kr/api/StatisticSearch/{K}/json/kr/1/100000/{stat}/{cyc}/{s}/{e}/{item}'
    j = json.load(urllib.request.urlopen(u, timeout=40))
    rows = j['StatisticSearch']['row']
    return {r['TIME']: float(r['DATA_VALUE']) for r in rows}, rows[0].get('ITEM_NAME1'), rows[0].get('UNIT_NAME')
dep1, n1, u1 = ecos('121Y002', 'M', '199601', '202610', 'BEABAA2118')
cpi, n2, u2 = ecos('901Y009', 'M', '199601', '202610', '0')
json.dump(dict(dep1=dep1, cpi=cpi, got=time.strftime('%Y-%m-%d %H:%M')), open(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\realdep1112\raw\ecos_1112.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('예금:', n1, u1, min(dep1), '~', max(dep1)); print('물가:', n2, u2, min(cpi), '~', max(cpi))
T = .846; P = 1e8
rows = []
for y in range(int(min(dep1)[:4]), 2026):
    a, b = f'{y}09', f'{y+1}09'
    if a not in dep1 or b not in cpi or a not in cpi: continue
    r = dep1[a]; pi = cpi[b]/cpi[a]-1
    nom = P*r/100*T; real = P*(1+r/100*T)/(1+pi) - P
    rows.append((y, r, pi*100, nom, real))
print('== 9월에 1억 1년 맡김 → 다음 해 9월 만기 (세후 이자 · 1년 물가 · 물가 뺀 값)')
for y, r, pi, nom, real in rows:
    print(f' {y}.09 {r:.2f}% · 세후 {nom:,.0f} · 물가 {pi:.2f}% · 물가 뺀 {real:+,.0f}')
neg = [x for x in rows if x[4] < 0]
print(f'물가 뺀 값 마이너스: {len(neg)}/{len(rows)}해 ->', [x[0] for x in neg])
print('세후 금리 < 물가 (단순 비교):', sum(1 for x in rows if x[1]*T < x[2]))
# 지금 (2026.09) — 앞으로 1년 물가는 모름: 최근 1년 물가 오름(10월·9월 전년 같은 달 대비)으로 가정
for m in ('202609', '202610'):
    pm = f'{int(m[:4])-1}{m[4:]}'
    print(f' 최근 물가 {m}: 전년 같은 달 대비 {(cpi[m]/cpi[pm]-1)*100:.2f}%')
r = dep1['202609']; pi = cpi['202610']/cpi['202510']-1
print(f" 2026.09 {r}% · 세후 {P*r/100*T:,.0f} · 10월 물가 {pi*100:.2f}%가 이어진다면 물가 뺀 {P*(1+r/100*T)/(1+pi)-P:+,.0f}")
print(' 세후 금리:', {y: round(dep1[f'{y}09']*T, 3) for y in (2021, 2025, 2026)})
# 9월 시작이 아니라 모든 달 시작으로도 (표본 늘려 확인)
allm = [m for m in sorted(dep1) if f'{int(m[:4])+1}{m[4:]}' in cpi]
negm = [m for m in allm if (1+dep1[m]/100*T)/(cpi[f'{int(m[:4])+1}{m[4:]}']/cpi[m]) < 1]
print(f'모든 달 시작: {len(negm)}/{len(allm)}달 마이너스 ({allm[0]}~{allm[-1]})')
by = {}
for m in allm: by.setdefault(m[:4], []).append(m in negm)
print(' 해별 마이너스 달 수:', {y: sum(v) for y, v in by.items()})
