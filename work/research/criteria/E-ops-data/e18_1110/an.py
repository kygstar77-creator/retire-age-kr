import json, os, sys, statistics as st, random, math
sys.stdout.reconfigure(encoding='utf-8')
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S); import sst
d = json.load(open(os.path.join(S, 'comp.json'), encoding='utf-8'))
FIXED = ['UCE9Q2l8yGDiDph3nTIQvDzQ','UC4i1O9S9_RVztD333qiCp5Q','UCS_vefzRwq-vhxcswl2zMWw','UCEJIw_FUvkxK7ZoiejSj7HA','UC1eyYJRpM_g5WBp60mmRwCQ']
def test(v, name):
    sig_out = [[0,0],[0,0]]; rat = {True: [], False: []}
    for i in range(20, len(v)):
        cm = st.median(v[i-20:i]); s = st.median(v[i-3:i]) < cm; o = v[i] < cm
        sig_out[s][o] += 1; rat[s].append(math.log((v[i]+1)/(cm+1)))
    n1 = sum(sig_out[1]); n0 = sum(sig_out[0])
    p1 = sig_out[1][1]/n1 if n1 else float('nan'); p0 = sig_out[0][1]/n0 if n0 else float('nan')
    fe = sst.fisher(sig_out)
    ac = sst.spearman(v[:-1], v[1:])
    print(f'{name}: n={len(v)} 판정 {n1+n0} · 쉼 신호 {n1}({n1/(n1+n0):.0%}) · 다음 편 채널중앙 아래: 쉼 뒤 {p1:.0%} vs 아님 뒤 {p0:.0%} (Fisher p={fe:.2f}) · 다음편/채널중앙 중앙배율 쉼 {math.exp(st.median(rat[True])):.2f} vs 아님 {math.exp(st.median(rat[False])):.2f} · 연속 두 편 순위상관 {ac:.2f}')
    return sig_out
tot = [[0,0],[0,0]]
for cid in FIXED:
    c = d[cid]; v = [x['views'] for x in c['vids'] if x['sec'] <= 180 and '2026-05-01' <= x['pub'] < '2026-11-03']
    so = test(v, c['name'])
    for a in (0,1):
        for b in (0,1): tot[a][b] += so[a][b]
n1 = sum(tot[1]); n0 = sum(tot[0])
print(f'합계: 판정 {n1+n0}, 쉼 신호 {n1}({n1/(n1+n0):.0%}) · 쉼 뒤 아래 {tot[1][1]/n1:.1%} vs 아님 뒤 {tot[0][1]/n0:.1%} · Fisher p={sst.fisher(tot):.3f}')
