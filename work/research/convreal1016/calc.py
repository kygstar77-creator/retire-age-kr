# convreal1016 계산 — 서울 아파트 신규 계약, 같은 단지·같은 면적대에서 전세와 월세를 견줘 '실제 시장 전환율' 구하기
# 원자료: ../aptrent1013/raw (국토부 RTMSDataSvcAptRent, 2026-10-13 18:25 받음) 2026년 7~8월(9월 신고 미완 제외), 신규만
# 전환율 = 월세*12 / (전세 보증금 - 월세 계약 보증금)
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
def band(ar): return int(ar // 5) * 5
for y in (2025, 2026):
    D = [r for r in load(y, (7, 8)) if r['contractType'] == '신규' and r['_dep'] > 0]
    jeon = collections.defaultdict(list); wol = collections.defaultdict(list)
    for r in D:
        k = (r['aptSeq'], band(r['_ar']))
        (jeon if r['_rent'] == 0 else wol)[k].append(r)
    ks = [k for k in jeon if k in wol]
    print(f'## {y} 7~8월 신규: 전세 {sum(len(v) for v in jeon.values()):,}건 월세 {sum(len(v) for v in wol.values()):,}건 · 전세·월세 둘 다 있는 칸 {len(ks):,}')
    for minn in (1, 2):
        rates = []; rows = []
        for k in ks:
            if len(jeon[k]) < minn or len(wol[k]) < minn: continue
            jd = st.median(x['_dep'] for x in jeon[k]); wd = st.median(x['_dep'] for x in wol[k]); wr = st.median(x['_rent'] for x in wol[k])
            if jd - wd <= 0: continue
            rt = wr * 12 / (jd - wd) * 100
            rates.append(rt); rows.append((k, rt, jd, wd, wr, jeon[k][0]['sggCd']))
        if not rates: continue
        qs = st.quantiles(rates, n=4)
        print(f' 칸당 {minn}건 이상: {len(rates):,}칸 · 전환율 중앙 {st.median(rates):.2f}% 평균 {st.mean(rates):.2f}% · 1사분위 {qs[0]:.2f} 3사분위 {qs[2]:.2f} · 5% 이하 {100*sum(r<=5 for r in rates)/len(rates):.1f}% · 5~6% {100*sum(5<r<=6 for r in rates)/len(rates):.1f}% · 6% 초과 {100*sum(r>6 for r in rates)/len(rates):.1f}% · 4% 미만 {100*sum(r<4 for r in rates)/len(rates):.1f}%')
        if minn == 1 and y == 2026:
            R1 = rows
        if minn == 2 and y == 2026:
            R2 = rows
    if y == 2026:
        print('\n구별 (칸당 1건 이상, 2026):')
        res = []
        for code, name in SGG.items():
            rr = [r[1] for r in R1 if r[5] == code]
            if rr: res.append((name, len(rr), st.median(rr)))
        for n, c, m in sorted(res, key=lambda x: -x[2]): print(f'  {n:5} 칸 {c:4} 전환율 중앙 {m:.2f}%')
        # 84㎡ 대표 칸
        r84 = [r[1] for r in R1 if r[0][1] == 80]
        print('전용 80~85㎡ 칸:', len(r84), f'중앙 {st.median(r84):.2f}%')
        # 보증금 구간: 월세 보증금 별 전환율
        print('\n월세 계약 보증금별 (2026, 칸 기준 아님: 전 월세 건):')
        Wl = [r for r in load(2026, (7, 8)) if r['contractType'] == '신규' and r['_rent'] > 0]
        print(' 월세 신규', len(Wl), '보증금 중앙', st.median(r['_dep'] for r in Wl), '월세 중앙', st.median(r['_rent'] for r in Wl))
        # 전세 보증금 대비 월세 전환 시 5% 상한이라면: 칸에서 상한 월세 vs 실제
        over = 0; tot = 0; gaps = []
        for k, rt, jd, wd, wr, sg in R1:
            tot += 1
            cap = (jd - wd) * 0.05 / 12
            gaps.append(wr - cap)
            if wr > cap: over += 1
        print(f' 5% 상한보다 높은 칸 {over}/{tot} ({100*over/tot:.1f}%) · 월세-상한 차이 중앙 {st.median(gaps):+.1f}만원/월 평균 {st.mean(gaps):+.1f}')

print('\n######## 줄어든 보증금 크기별 (2026, 칸당 1건 이상)')
for lo, hi, lab in ((0, 10000, '1억 미만'), (10000, 30000, '1~3억'), (30000, 60000, '3~6억'), (60000, 10**9, '6억 이상')):
    rr = [r[1] for r in R1 if lo <= r[2] - r[3] < hi]
    if rr: print(f' 줄어든 보증금 {lab}: {len(rr)}칸 · 전환율 중앙 {st.median(rr):.2f}% · 5% 초과 {100*sum(x>5 for x in rr)/len(rr):.1f}%')
print('\n######## 월세 계약 보증금 크기별')
for lo, hi, lab in ((0, 5000, '5천만 미만'), (5000, 10000, '5천~1억'), (10000, 30000, '1~3억'), (30000, 10**9, '3억 이상')):
    rr = [r[1] for r in R1 if lo <= r[3] < hi]
    if rr: print(f' 월세 계약 보증금 {lab}: {len(rr)}칸 · 전환율 중앙 {st.median(rr):.2f}% · 5% 초과 {100*sum(x>5 for x in rr)/len(rr):.1f}%')
rr = [r[1] for r in R1 if r[2] - r[3] >= 30000]
print(f' 줄어든 보증금 3억 이상 합계: {len(rr)}칸 · 전환율 중앙 {st.median(rr):.2f}% · 5% 초과 {100*sum(x>5 for x in rr)/len(rr):.1f}%')

print('\n######## 계약 날짜의 상한으로 견주기 (레드팀 T1·T2, 2026-10-16 09시)')
# 한국은행 기준금리: 2025-05-29 2.50% · 2026-07-16 2.75% · 2026-08-27 3.00% → 상한 = 기준금리+2%p
import datetime as dt
def cap_at(d):
    if d >= dt.date(2026, 8, 27): return 5.0
    if d >= dt.date(2026, 7, 16): return 4.75
    return 4.5
def ddate(r): return dt.date(int(r['dealYear']), int(r['dealMonth']), int(r['dealDay']))
Wl = [r for r in load(2026, (7, 8)) if r['contractType'] == '신규' and r['_rent'] > 0 and r['_dep'] >= 0]
cc = collections.Counter(cap_at(ddate(r)) for r in Wl)
print(' 2026 7~8월 신규 월세 계약의 계약일 상한:', {k: f'{v}건 {100*v/len(Wl):.1f}%' for k, v in sorted(cc.items())})
# 칸별: 월세 계약일 가운데 날짜의 상한
D = [r for r in load(2026, (7, 8)) if r['contractType'] == '신규' and r['_dep'] > 0]
jeon = collections.defaultdict(list); wol = collections.defaultdict(list)
for r in D: ((jeon if r['_rent'] == 0 else wol)[(r['aptSeq'], band(r['_ar']))]).append(r)
over = 0; tot = 0; cc2 = collections.Counter()
for k in jeon:
    if k not in wol: continue
    jd = st.median(x['_dep'] for x in jeon[k]); wd = st.median(x['_dep'] for x in wol[k]); wr = st.median(x['_rent'] for x in wol[k])
    if jd - wd <= 0: continue
    rt = wr * 12 / (jd - wd) * 100
    ds = sorted(ddate(x) for x in wol[k]); cap = cap_at(ds[len(ds) // 2])
    tot += 1; cc2[cap] += 1
    if rt > cap: over += 1
print(f' 칸 {tot} · 칸별 상한 분포 {dict(cc2)} · 그때 상한보다 높은 칸 {over} ({100*over/tot:.1f}%)')
print(' 2025 7~8월은 내내 기준금리 2.50% → 상한 4.5%')
