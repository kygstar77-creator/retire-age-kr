# 서울 아파트 전월세 실거래(국토부 RTMSDataSvcAptRent, 2026-10-22 받음 1~6월 + 10/13 받은 7~8월) — 1~8월 계약, 월세 비중(월세>0)
# 9월은 신고 기한(30일) 안이라 뺐다
import sys, os, json, glob, re, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
SGG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
def num(s): return int(re.sub(r'[^\d]', '', str(s or '0')) or 0)
def load(y):
    out = []
    for m in range(1, 9):
        for f in glob.glob(os.path.join(H, 'raw', 'rent', f'*_{y}{m:02d}_rent.json')):
            out += json.load(open(f, encoding='utf-8'))
    return out
res = {}
lines = []
for y in (2025, 2026):
    D = load(y); n = len(D); w = sum(num(r['monthlyRent']) > 0 for r in D)
    lines.append(f'## {y} 1~8월 전체 {n:,}건 · 월세 {w:,}건 · 월세 비중 {100*w/n:.1f}%')
    ct = collections.Counter(r.get('contractType') or '(빈칸)' for r in D)
    for t, c in ct.most_common():
        ww = sum(num(r['monthlyRent']) > 0 for r in D if (r.get('contractType') or '(빈칸)') == t)
        lines.append(f'   {t}: {c:,}건 · 월세 {ww:,} ({100*ww/c:.1f}%)')
    byg = collections.defaultdict(lambda: [0, 0])
    for r in D:
        g = SGG.get(r['sggCd'], r['sggCd']); byg[g][0] += 1; byg[g][1] += num(r['monthlyRent']) > 0
    res[y] = {g: (v[0], v[1], 100 * v[1] / v[0]) for g, v in byg.items()}
    mon = collections.defaultdict(lambda: [0, 0])
    for r in D:
        k = int(r['dealMonth']); mon[k][0] += 1; mon[k][1] += num(r['monthlyRent']) > 0
    lines.append('   월별 월세 비중: ' + ' · '.join(f'{k}월 {100*v[1]/v[0]:.1f}%' for k, v in sorted(mon.items())))
    lines.append(f'   월세 계약 월세 중앙: {sorted(num(r["monthlyRent"]) for r in D if num(r["monthlyRent"])>0)[w//2]:,}만원')
lines.append('## 구별 월세 비중 2026 1~8월 (2025 같은 기간 → 차이)')
rows = sorted(res[2026].items(), key=lambda kv: -kv[1][2])
for g, (n, w, p) in rows:
    p0 = res[2025].get(g, (0, 0, 0))[2]
    lines.append(f'   {g}: {n:,}건 · 월세 {p:.1f}% (2025 {p0:.1f}%, {p-p0:+.1f}%p)')
s = '\n'.join(lines); print(s); open(os.path.join(H, 'calc2_out.txt'), 'w', encoding='utf-8').write(s + '\n')
# 갱신 계약 중 종전 전세(preMonthlyRent 0, preDeposit 있음) → 이번에 월세가 붙은 비율
lines2 = ['## 갱신 계약: 종전 조건이 적힌 것 중 전세→월세로 바뀐 비율']
for y in (2025, 2026):
    G = [r for r in load(y) if r.get('contractType') == '갱신' and num(r.get('preDeposit')) > 0]
    pj = [r for r in G if num(r.get('preMonthlyRent')) == 0]
    sw = [r for r in pj if num(r['monthlyRent']) > 0]
    pw = [r for r in G if num(r.get('preMonthlyRent')) > 0]
    back = [r for r in pw if num(r['monthlyRent']) == 0]
    rr = sorted(num(r['monthlyRent']) for r in sw)
    dd = sorted(num(r['preDeposit']) - num(r['deposit']) for r in sw)
    lines2.append(f'   {y}: 갱신(종전 적힘) {len(G):,} · 종전 전세 {len(pj):,} 중 월세 붙음 {len(sw):,} ({100*len(sw)/len(pj):.1f}%) · 월세 중앙 {rr[len(rr)//2]:,}만원 · 보증금 줄인 폭 중앙 {dd[len(dd)//2]:,}만원 · 종전 월세 {len(pw):,} 중 전세로 {len(back):,} ({100*len(back)/len(pw):.1f}%)')
    ru = [r for r in G if r.get('useRRRight') == '사용']
    lines2.append(f'      갱신요구권 사용 {len(ru):,}건({100*len(ru)/len(G):.1f}%)')
s2 = '\n'.join(lines2); print(s2); open(os.path.join(H, 'calc2_out.txt'), 'a', encoding='utf-8').write(s2 + '\n')
lines3 = ['## 전세→월세 붙은 갱신: 보증금 그대로·늘림(줄인 폭 0 이하) 비율']
for y in (2025, 2026):
    sw = [r for r in load(y) if r.get('contractType') == '갱신' and num(r.get('preDeposit')) > 0 and num(r.get('preMonthlyRent')) == 0 and num(r['monthlyRent']) > 0]
    z = sum(num(r['preDeposit']) - num(r['deposit']) <= 0 for r in sw); lo = sum(num(r['preDeposit']) - num(r['deposit']) > 0 for r in sw)
    lines3.append(f'   {y}: {len(sw):,}건 중 보증금 안 줄임 {z:,} ({100*z/len(sw):.1f}%) · 줄임 {lo:,}')
s3 = '\n'.join(lines3); print(s3); open(os.path.join(H, 'calc2_out.txt'), 'a', encoding='utf-8').write(s3 + '\n')
# 레드팀 10/22: '보증금 안 줄임' 안에 '보증금 올림'이 섞임 → 그대로·올림·줄임 나눠 셈, 종전 월세 갱신 비중
for y in (2025, 2026):
    G = [r for r in load(y) if r.get('contractType') == '갱신' and num(r.get('preDeposit')) > 0]
    sw = [r for r in G if num(r.get('preMonthlyRent')) == 0 and num(r['monthlyRent']) > 0]
    d = [num(r['preDeposit']) - num(r['deposit']) for r in sw]
    s4 = f'   {y}: 전세→월세 붙은 갱신 {len(sw):,} · 보증금 그대로 {sum(x==0 for x in d):,}({100*sum(x==0 for x in d)/len(d):.1f}%) · 올림 {sum(x<0 for x in d):,}({100*sum(x<0 for x in d)/len(d):.1f}%) · 줄임 {sum(x>0 for x in d):,}({100*sum(x>0 for x in d)/len(d):.1f}%) · 종전 월세 갱신 비중 {100*sum(num(r.get("preMonthlyRent"))>0 for r in G)/len(G):.1f}%'
    print(s4); open(os.path.join(H, 'calc2_out.txt'), 'a', encoding='utf-8').write(s4 + '\n')
