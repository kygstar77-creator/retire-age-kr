# h2cafe1019 새로 확인한 것 — 2026-10-19 밤 다시 받은 국토부 실거래(raw/)로 대표 단지 84㎡대(전용 80~85㎡) 최근 계약.
# 매매: 해제(cdealType) 표시·공공기관 매수는 따로 센다. 전세: 월세 0 · 신규.
import sys, os, json, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
RT_OLD = os.path.join(H, '..', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
def is84(r): return 80 <= num(r['excluUseAr']) < 85
def nm(r): return r['aptNm'].replace(' ', '')
def d(r): return f"{r['dealYear']}-{str(r['dealMonth']).zfill(2)}-{str(r['dealDay']).zfill(2)}"
DONG = {'11680': '대치동', '11710': '잠실동', '11650': '반포동'}
PICK = ['주공아파트5단지', '리센츠', '잠실엘스', '트리지움', '우성아파트', '은마', '래미안대치팰리스', '대치르엘', '한보미도맨션1', '래미안원베일리', '아크로리버파크', '래미안퍼스티지', '반포자이', '반포미도']
T, R, X = [], [], []
for lawd, umd in DONG.items():
    for ym in ('202608', '202609', '202610'):
        t = json.load(open(os.path.join(H, 'raw', f'{lawd}_{ym}_trade.json'), encoding='utf-8'))
        r = json.load(open(os.path.join(H, 'raw', f'{lawd}_{ym}_rent.json'), encoding='utf-8'))
        for x in t:
            if x.get('umdNm') != umd: continue
            (X if x.get('cdealType') else T).append(x)
        R += [x for x in r if x.get('umdNm') == umd]
print('# h2cafe1019 calc_out — 2026-10-19 21:26 다시 받은 국토부 실거래(2026-08~10 계약), 단위 억원')
print(f'매매(해제 빼고) {len(T)}건 · 해제 표시 {len(X)}건 · 전월세 {len(R)}건\n')
print('## 1. 대표 단지 84㎡대 매매 — 8~10월 계약 전부(계약일 · 값 · 층 · 거래 방식)')
for a in PICK:
    rows = sorted([x for x in T if nm(x) == a and is84(x) and x.get('buyerGbn') != '공공기관'], key=d)
    xs = [x for x in X if nm(x) == a and is84(x)]
    if not rows and not xs: print(f'- {a}: 8~10월 84㎡대 매매 0건'); continue
    print(f"- {a}: {len(rows)}건" + (f" (해제 표시 {len(xs)}건 따로)" if xs else '') + ' — ' + ' / '.join(f"{d(x)} {num(x['dealAmount'])/10000:.2f}억 {x.get('floor')}층 {x.get('dealingGbn')}" for x in rows[-6:]))
print('\n## 2. 10월 계약(10/19 신고분까지) 84㎡대 매매 — 세 동네 전부')
for x in sorted([x for x in T if x['dealMonth'] in ('10',) and is84(x)], key=d):
    print(f"- {DONG[x['sggCd']] if x.get('sggCd') in DONG else x['umdNm']} {nm(x)} {d(x)} {num(x['dealAmount'])/10000:.2f}억 {x.get('floor')}층 {x.get('dealingGbn')} 건축 {x.get('buildYear')}")
print('\n## 3. 대표 단지 84㎡대 신규 순수전세 — 9~10월 계약 가운데 값·건수·최근')
for a in PICK:
    js = sorted([x for x in R if nm(x) == a and is84(x) and x.get('contractType') == '신규' and num(x['monthlyRent']) == 0 and x['dealMonth'] in ('9', '09', '10')], key=d)
    if not js: print(f'- {a}: 0건'); continue
    v = [num(x['deposit']) for x in js]
    print(f"- {a}: {len(js)}건 가운데 {st.median(v)/10000:.2f}억 · 최저 {min(v)/10000:.2f} 최고 {max(v)/10000:.2f} · 가장 최근 {d(js[-1])} {v[-1]/10000:.2f}억")
print('\n## 4. 10/12 받은 파일(work/research/rt)에 없던 84㎡대 매매(같은 단지·계약일·값·층으로 맞춤) — 늦게 신고된 것')
for lawd, umd in DONG.items():
    for ym in ('202609', '202610'):
        p = os.path.join(RT_OLD, f'{lawd}_{ym}_trade.json')
        old = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
        key = lambda x: (nm(x), d(x), x.get('dealAmount'), x.get('floor'))
        ok = {key(x) for x in old}
        new = [x for x in T if x['sggCd'] == lawd and f"{x['dealYear']}{str(x['dealMonth']).zfill(2)}" == ym and is84(x) and key(x) not in ok]
        print(f"- {umd} {ym}: 받은 파일 시각 {__import__('datetime').datetime.fromtimestamp(os.path.getmtime(p)):%m-%d %H:%M} · 새로 보인 84㎡대 {len(new)}건" + (': ' + ' / '.join(f"{nm(x)} {d(x)} {num(x['dealAmount'])/10000:.2f}억 {x.get('floor')}층" for x in sorted(new, key=d)) if new else ''))
