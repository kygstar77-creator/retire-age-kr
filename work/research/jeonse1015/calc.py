# jeonse1015 계산 — 서울 25개 구 아파트 전세 실거래(국토부 RTMSDataSvcAptRent, ../aptrent1013/raw/ 10/13 18:25 받은 것 재사용)
# 질문: 같은 단지·같은 면적대 신규 전세 보증금이 1년 전(2025 7~8월)보다 얼마나 올랐나 (2026 7~8월, 계약일 기준; 9월은 신고 덜 들어와 뺌)
import sys, os, json, glob, re, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
RAW = os.path.join(H, '..', 'aptrent1013', 'raw')
SGG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
def load(y, months):
    out = []
    for m in months:
        for f in glob.glob(os.path.join(RAW, f'*_{y}{m:02d}_rent.json')):
            for r in json.load(open(f, encoding='utf-8')):
                r['_rent'] = num(r['monthlyRent']); r['_dep'] = num(r['deposit']); r['_ar'] = float(r['excluUseAr'] or 0); out.append(r)
    return out
def pct(a, b): return 100 * a / b if b else 0
def band(ar): return int(ar // 5) * 5
A = [r for r in load(2025, (7, 8)) if r['_rent'] == 0 and r['contractType'] == '신규' and r['_dep'] > 0]
B = [r for r in load(2026, (7, 8)) if r['_rent'] == 0 and r['contractType'] == '신규' and r['_dep'] > 0]
print(f'신규 전세(7~8월) 2025 {len(A):,}건 · 2026 {len(B):,}건 · 보증금 중앙 {st.median(r["_dep"] for r in A):,.0f} → {st.median(r["_dep"] for r in B):,.0f}만원')
print(f'  평균 {st.mean(r["_dep"] for r in A):,.0f} → {st.mean(r["_dep"] for r in B):,.0f}')
ga, gb = collections.defaultdict(list), collections.defaultdict(list)
for r in A: ga[(r['aptSeq'], band(r['_ar']))].append(r)
for r in B: gb[(r['aptSeq'], band(r['_ar']))].append(r)
for minn in (1, 2):
    ks = [k for k in ga if k in gb and len(ga[k]) >= minn and len(gb[k]) >= minn]
    chg = [st.median(x['_dep'] for x in gb[k]) / st.median(x['_dep'] for x in ga[k]) - 1 for k in ks]
    dd = [st.median(x['_dep'] for x in gb[k]) - st.median(x['_dep'] for x in ga[k]) for k in ks]
    print(f'칸 해마다 {minn}건 이상: {len(ks):,}칸 · 변화율 중앙 {100*st.median(chg):+.1f}% · 평균 {100*st.mean(chg):+.1f}% · 금액 변화 중앙 {st.median(dd):+,.0f}만원 · 오른 {sum(c>0 for c in chg)} 같음 {sum(c==0 for c in chg)} 내림 {sum(c<0 for c in chg)} ({pct(sum(c>0 for c in chg),len(chg)):.1f}%)')
    print(f'   +10% 이상 {pct(sum(c>=0.1 for c in chg),len(chg)):.1f}% · -10% 이하 {pct(sum(c<=-0.1 for c in chg),len(chg)):.1f}%')
ks = [k for k in ga if k in gb]
print('\n전용 80~85㎡ 칸:')
k84 = [k for k in ks if k[1] == 80]
c84 = [st.median(x['_dep'] for x in gb[k]) / st.median(x['_dep'] for x in ga[k]) - 1 for k in k84]
d84 = [st.median(x['_dep'] for x in gb[k]) - st.median(x['_dep'] for x in ga[k]) for k in k84]
print(f'  {len(k84)}칸 · 변화율 중앙 {100*st.median(c84):+.1f}% · 금액 중앙 {st.median(d84):+,.0f}만원 · 오른 {sum(c>0 for c in c84)} 내림 {sum(c<0 for c in c84)}')
print('\n구별 (칸 해마다 1건 이상):')
res = []
for code, name in SGG.items():
    kk = [k for k in ks if ga[k][0]['sggCd'] == code]
    ch = [st.median(x['_dep'] for x in gb[k]) / st.median(x['_dep'] for x in ga[k]) - 1 for k in kk]
    dd = [st.median(x['_dep'] for x in gb[k]) - st.median(x['_dep'] for x in ga[k]) for k in kk]
    na = sum(1 for r in A if r['sggCd'] == code); nb = sum(1 for r in B if r['sggCd'] == code)
    k84g = [k for k in kk if k[1] == 80]
    m84 = [st.median(x['_dep'] for x in ga[k]) for k in k84g]; n84 = [st.median(x['_dep'] for x in gb[k]) for k in k84g]
    res.append((name, len(kk), 100 * st.median(ch) if ch else 0, st.median(dd) if dd else 0, pct(sum(c > 0 for c in ch), len(ch)), na, nb, len(k84g), st.median(m84) if m84 else 0, st.median(n84) if n84 else 0))
for r in sorted(res, key=lambda x: -x[2]):
    print(f'  {r[0]:5} 칸 {r[1]:4} · 변화 중앙 {r[2]:+5.1f}% · 금액 {r[3]:+7,.0f}만원 · 오른 칸 {r[4]:4.1f}% | 신규전세 {r[5]}→{r[6]}건 | 84㎡칸 {r[7]} 보증금 중앙 {r[8]:,.0f}→{r[9]:,.0f}')
print('  칸 30 미만:', [r[0] for r in res if r[1] < 30])
print('  내린 구:', [r[0] for r in res if r[2] < 0], ' 같은 구:', [r[0] for r in res if r[2] == 0])
# 건수 변화
na, nb = len(A), len(B); print(f'\n건수 {na:,} → {nb:,} ({100*(nb/na-1):+.1f}%)')
for y, D in ((2025, A), (2026, B)):
    print(y, '보증금 5억 이상 비중', f'{pct(sum(r["_dep"]>=50000 for r in D), len(D)):.1f}%', '10억 이상', f'{pct(sum(r["_dep"]>=100000 for r in D), len(D)):.1f}%', '3억 미만', f'{pct(sum(r["_dep"]<30000 for r in D), len(D)):.1f}%')

print('\n######## 추가')
for y in (2025, 2026):
    D = [r for r in load(y, (7, 8)) if r['_rent'] == 0 and r['_dep'] > 0]
    n = sum(r['contractType'] == '신규' for r in D); g = sum(r['contractType'] == '갱신' for r in D)
    print(y, f'7~8월 전세 전체 {len(D):,} · 신규 {n:,} · 갱신 {g:,} · 갱신 비중 {pct(g, n+g):.1f}% · 종류 {collections.Counter(r["contractType"] for r in D)}')
# 오른 칸 중 1억 이상 오른 칸
ks = [k for k in ga if k in gb]
dd = [st.median(x['_dep'] for x in gb[k]) - st.median(x['_dep'] for x in ga[k]) for k in ks]
print(f'칸 {len(ks):,}: 1억 이상 오른 칸 {sum(d>=10000 for d in dd)} ({pct(sum(d>=10000 for d in dd), len(dd)):.1f}%) · 1억 이상 내린 칸 {sum(d<=-10000 for d in dd)}')
# 같은 단지 84㎡대(80~85) 칸 서울 전체 보증금 중앙 변화 (칸 중앙 → 칸 중앙)
k84 = [k for k in ks if k[1] == 80]
print('84㎡ 칸', len(k84), '2025 칸중앙의 중앙', st.median(st.median(x['_dep'] for x in ga[k]) for k in k84), '→ 2026', st.median(st.median(x['_dep'] for x in gb[k]) for k in k84))
# 표 후보: 칸 90 이상 구의 상위/하위
