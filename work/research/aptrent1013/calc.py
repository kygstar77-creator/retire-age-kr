# aptrent1013 계산 — 서울 25개 구 아파트 전월세 실거래(국토부 RTMSDataSvcAptRent, raw/ 10/13 18:25 받음)
# 질문: 월세 100만원 넘는 아파트 계약 비중이 1년 전보다 얼마나 늘었나 (7~9월 계약일 기준, 2025 vs 2026)
# 월세 계약 = monthlyRent > 0. 신규·갱신 구분은 contractType.
import sys, os, json, glob, re, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
SGG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
def load(y, months):
    out = []
    for m in months:
        for f in glob.glob(os.path.join(H, 'raw', f'*_{y}{m:02d}_rent.json')):
            for r in json.load(open(f, encoding='utf-8')):
                r['_rent'] = num(r['monthlyRent']); r['_dep'] = num(r['deposit']); r['_ar'] = float(r['excluUseAr'] or 0); out.append(r)
    return out
def pct(a, b): return 100 * a / b if b else 0
def band(ar): return int(ar // 5) * 5   # 전용 5㎡ 단위
for label, months in (('7~9월', (7, 8, 9)), ('7~8월(9월 신고 덜 들어온 것 빼고)', (7, 8))):
    print(f'\n######## 계약월 {label}')
    A, B = load(2025, months), load(2026, months)
    for nm, D in (('2025', A), ('2026', B)):
        w = [r for r in D if r['_rent'] > 0]; j = [r for r in D if r['_rent'] == 0]
        ct = collections.Counter(r['contractType'] for r in w)
        print(f'{nm}: 전체 {len(D):,} · 월세 {len(w):,} ({pct(len(w), len(D)):.1f}%) · 전세 {len(j):,} · 월세 계약구분 {dict(ct)}')
        for flt, fn in (('전체 월세', lambda r: True), ('신규 월세', lambda r: r['contractType'] == '신규'), ('갱신 월세', lambda r: r['contractType'] == '갱신')):
            ww = [r for r in w if fn(r)]
            o100 = sum(r['_rent'] >= 100 for r in ww); o200 = sum(r['_rent'] >= 200 for r in ww); o300 = sum(r['_rent'] >= 300 for r in ww)
            med = st.median(r['_rent'] for r in ww) if ww else 0
            print(f'   {flt}: {len(ww):,}건 · 100만원 이상 {o100:,} ({pct(o100, len(ww)):.1f}%) · 200만원 이상 {pct(o200, len(ww)):.1f}% · 300만원 이상 {pct(o300, len(ww)):.1f}% · 월세 중앙값 {med:g}만원')
    if label != '7~9월': continue
    # 구별 (신규 월세)
    print('\n구별 — 신규 월세 계약, 월 100만원 이상 비중 (2025 → 2026, 건수)')
    rows = []
    for code, name in SGG.items():
        a = [r for r in A if r['sggCd'] == code and r['_rent'] > 0 and r['contractType'] == '신규']
        b = [r for r in B if r['sggCd'] == code and r['_rent'] > 0 and r['contractType'] == '신규']
        pa, pb = pct(sum(r['_rent'] >= 100 for r in a), len(a)), pct(sum(r['_rent'] >= 100 for r in b), len(b))
        rows.append((name, len(a), pa, len(b), pb, pb - pa, st.median(r['_rent'] for r in a) if a else 0, st.median(r['_rent'] for r in b) if b else 0))
    for r in sorted(rows, key=lambda x: -x[5]):
        print(f'  {r[0]:5} 2025 {r[1]:4}건 {r[2]:5.1f}% → 2026 {r[3]:4}건 {r[4]:5.1f}%  차이 {r[5]:+5.1f}%p · 중앙 {r[6]:g}→{r[7]:g}만원')
    print('  2026 비중 높은 순:', ', '.join(f'{r[0]} {r[4]:.1f}%' for r in sorted(rows, key=lambda x: -x[4])[:5]))
    print('  2026 비중 낮은 순:', ', '.join(f'{r[0]} {r[4]:.1f}%' for r in sorted(rows, key=lambda x: x[4])[:5]))
    up = sum(r[5] > 0 for r in rows); print(f'  비중 늘어난 구 {up}곳 / 25 · 표본 30 미만 구: {[r[0] for r in rows if min(r[1], r[3]) < 30]}')
    # 같은 단지·같은 면적대(5㎡) — 신규 월세 계약, 양쪽 해에 각각 1건 이상
    print('\n같은 단지(aptSeq)·같은 면적대(전용 5㎡ 단위) 신규 월세 — 두 해 모두 계약 있는 칸')
    for minn in (1, 2):
        ga, gb = collections.defaultdict(list), collections.defaultdict(list)
        for r in A:
            if r['_rent'] > 0 and r['contractType'] == '신규': ga[(r['aptSeq'], band(r['_ar']))].append(r)
        for r in B:
            if r['_rent'] > 0 and r['contractType'] == '신규': gb[(r['aptSeq'], band(r['_ar']))].append(r)
        ks = [k for k in ga if k in gb and len(ga[k]) >= minn and len(gb[k]) >= minn]
        ra = [r for k in ks for r in ga[k]]; rb = [r for k in ks for r in gb[k]]
        chg = [st.median(x['_rent'] for x in gb[k]) / st.median(x['_rent'] for x in ga[k]) - 1 for k in ks]
        dchg = [st.median(x['_dep'] for x in gb[k]) - st.median(x['_dep'] for x in ga[k]) for k in ks]
        # 보증금 차이를 감안한 환산 월세(전환율 연 5% 가정은 하지 않는다 — 보증금 중앙 변화만 같이 본다)
        print(f'  칸마다 해마다 {minn}건 이상: {len(ks):,}칸 · 계약 2025 {len(ra):,} / 2026 {len(rb):,}')
        print(f'    100만원 이상 비중 {pct(sum(r["_rent"]>=100 for r in ra), len(ra)):.1f}% → {pct(sum(r["_rent"]>=100 for r in rb), len(rb)):.1f}%')
        print(f'    칸별 월세 중앙값 변화의 중앙값 {100*st.median(chg):+.1f}% · 오른 칸 {sum(c>0 for c in chg)} / 같은 칸 {sum(c==0 for c in chg)} / 내린 칸 {sum(c<0 for c in chg)}')
        print(f'    칸별 보증금 중앙값 변화의 중앙값 {st.median(dchg):+,.0f}만원 · 보증금 줄어든 칸 {sum(d<0 for d in dchg)} / 늘어난 칸 {sum(d>0 for d in dchg)}')
        both = [ (ga[k], gb[k]) for k in ks]
        # 보증금이 같은 수준(±10%)인 칸만
        same = [k for k in ks if st.median(x['_dep'] for x in ga[k]) > 0 and abs(st.median(x['_dep'] for x in gb[k]) / st.median(x['_dep'] for x in ga[k]) - 1) <= 0.1]
        if same:
            c2 = [st.median(x['_rent'] for x in gb[k]) / st.median(x['_rent'] for x in ga[k]) - 1 for k in same]
            print(f'    보증금 중앙값이 ±10% 안인 칸 {len(same)}칸: 월세 변화 중앙값 {100*st.median(c2):+.1f}% · 오른 칸 {sum(c>0 for c in c2)} 내린 칸 {sum(c<0 for c in c2)}')
        if minn == 1:
            # 84㎡ 안팎(전용 80~85) 대표 면적
            k84 = [k for k in ks if k[1] in (80,)]
            c84 = [st.median(x['_rent'] for x in gb[k]) / st.median(x['_rent'] for x in ga[k]) - 1 for k in k84]
            if c84: print(f'    전용 80~85㎡ 칸 {len(k84)}개: 월세 변화 중앙값 {100*st.median(c84):+.1f}%, 오른 칸 {sum(c>0 for c in c84)} 내린 칸 {sum(c<0 for c in c84)}')

# ── 왜 100만원 이상 비중이 줄었나: 보증금 큰 월세(반전세)가 늘었는지 (7~9월 신규 월세)
print('\n######## 7~9월 신규 월세 — 보증금·월세 구간')
A, B = load(2025, (7, 8, 9)), load(2026, (7, 8, 9))
for nm, D in (('2025', A), ('2026', B)):
    w = [r for r in D if r['_rent'] > 0 and r['contractType'] == '신규']
    n = len(w)
    print(f'{nm}: {n:,}건 · 보증금 중앙 {st.median(r["_dep"] for r in w):,.0f}만원 · 월세 50만원 미만 {sum(r["_rent"]<50 for r in w):,}건 ({pct(sum(r["_rent"]<50 for r in w), n):.1f}%)'
          f' · 50~100만원 미만 {pct(sum(50<=r["_rent"]<100 for r in w), n):.1f}% · 보증금 3억 이상 {sum(r["_dep"]>=30000 for r in w):,}건 ({pct(sum(r["_dep"]>=30000 for r in w), n):.1f}%)'
          f' · 100만원 이상 건수 {sum(r["_rent"]>=100 for r in w):,}')
    j = [r for r in D if r['_rent'] == 0 and r['contractType'] == '신규']
    print(f'   신규 전세 {len(j):,}건 · 신규 전체 중 월세 {pct(n, n+len(j)):.1f}%')
# 중랑구 2026 신규 월세 많은 단지
print('\n중랑구 신규 월세 단지별 상위(2026 7~9월)')
for nm, D in (('2025', A), ('2026', B)):
    c = collections.Counter((r['aptNm'], r['buildYear']) for r in D if r['sggCd'] == '11260' and r['_rent'] > 0 and r['contractType'] == '신규')
    for (a, y), k in c.most_common(3):
        rr = [r for r in D if r['aptNm'] == a and r['sggCd'] == '11260' and r['_rent'] > 0 and r['contractType'] == '신규']
        print(f'  {nm} {a}({y}) {k}건 · 월세 중앙 {st.median(r["_rent"] for r in rr):g}만원 · 보증금 중앙 {st.median(r["_dep"] for r in rr):,.0f}만원')
# 새 아파트(2025~2026 준공) 신규 월세가 전체에서 차지하는 몫
for nm, D in (('2025', A), ('2026', B)):
    w = [r for r in D if r['_rent'] > 0 and r['contractType'] == '신규']
    nw = [r for r in w if num(r['buildYear']) >= int(nm) - 1]
    print(f'{nm}: 준공 {int(nm)-1}년 이후 단지 신규 월세 {len(nw):,}건 ({pct(len(nw), len(w)):.1f}%) · 그중 100만원 이상 {pct(sum(r["_rent"]>=100 for r in nw), len(nw)):.1f}%')
    ow = [r for r in w if num(r['buildYear']) < int(nm) - 1]
    print(f'      그 밖 단지 {len(ow):,}건 · 100만원 이상 {pct(sum(r["_rent"]>=100 for r in ow), len(ow)):.1f}%')

# 구별 — 같은 단지·같은 면적대 칸 월세 변화(구성 효과 뺌) + 준공 1년 넘은 단지만 100만원 이상 비중
print('\n######## 구별 같은 단지·면적대 신규 월세 변화 (칸 해마다 1건 이상) + 기존 단지 100만원 이상 비중')
ga, gb = collections.defaultdict(list), collections.defaultdict(list)
for r in A:
    if r['_rent'] > 0 and r['contractType'] == '신규': ga[(r['aptSeq'], band(r['_ar']))].append(r)
for r in B:
    if r['_rent'] > 0 and r['contractType'] == '신규': gb[(r['aptSeq'], band(r['_ar']))].append(r)
res = []
for code, name in SGG.items():
    ks = [k for k in ga if k in gb and ga[k][0]['sggCd'] == code]
    ch = [st.median(x['_rent'] for x in gb[k]) / st.median(x['_rent'] for x in ga[k]) - 1 for k in ks]
    oa = [r for r in A if r['sggCd'] == code and r['_rent'] > 0 and r['contractType'] == '신규' and num(r['buildYear']) < 2024]
    ob = [r for r in B if r['sggCd'] == code and r['_rent'] > 0 and r['contractType'] == '신규' and num(r['buildYear']) < 2025]
    res.append((name, len(ks), 100 * st.median(ch) if ch else 0, pct(sum(c > 0 for c in ch), len(ch)), len(oa), pct(sum(r['_rent'] >= 100 for r in oa), len(oa)), len(ob), pct(sum(r['_rent'] >= 100 for r in ob), len(ob))))
for r in sorted(res, key=lambda x: -x[2]):
    print(f'  {r[0]:5} 칸 {r[1]:4} · 월세 변화 중앙 {r[2]:+5.1f}% · 오른 칸 {r[3]:4.1f}% | 기존 단지 100만원 이상 {r[5]:4.1f}%({r[4]}) → {r[7]:4.1f}%({r[6]}) {r[7]-r[5]:+5.1f}%p')
print('  표본(칸) 30 미만 구:', [r[0] for r in res if r[1] < 30])
# 서울 전체 기존 단지 신규 월세 100만원 이상 비중 (2025: 2024년 이전 준공 / 2026: 2025년 이전 준공 — 같은 기준이면 둘 다 2024년 이전)
for nm, D in (('2025', A), ('2026', B)):
    w = [r for r in D if r['_rent'] > 0 and r['contractType'] == '신규' and num(r['buildYear']) < 2024]
    print(f'{nm}: 2023년까지 준공 단지 신규 월세 {len(w):,}건 · 100만원 이상 {pct(sum(r["_rent"]>=100 for r in w), len(w)):.1f}% · 중앙 {st.median(r["_rent"] for r in w):g}만원')
# 2026 준공 2025년 이후 단지 상위
c = collections.Counter((r['aptNm'], r['sggCd'], r['buildYear']) for r in B if r['_rent'] > 0 and r['contractType'] == '신규' and num(r['buildYear']) >= 2025)
print('2026 새 단지 신규 월세 상위:', '; '.join(f'{SGG[s]} {a}({y}) {k}건' for (a, s, y), k in c.most_common(6)))

# 7~8월(신고 끝난 달)만 신규 월세·전세 건수
for y in (2025, 2026):
    D = load(y, (7, 8)); w = sum(r['_rent'] > 0 and r['contractType'] == '신규' for r in D); j = sum(r['_rent'] == 0 and r['contractType'] == '신규' for r in D)
    print(f'{y} 7~8월 신규 월세 {w:,} · 신규 전세 {j:,} · 신규 중 월세 {pct(w, w+j):.1f}%')
