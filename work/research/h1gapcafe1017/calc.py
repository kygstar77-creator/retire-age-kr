# h1gapcafe1017 — 쇼츠 h1s_gap 짝 글. 국토부 실거래 원자료(work/research/rt) 84㎡대(전용 80~85) 가운데 값.
# 영상(10/11 받음, 고덕·둔촌은 9월까지)과 오늘(10/16) 다시 받은 값을 나란히 놓는다. 보증금 9.50억 = 래미안힐스테이트고덕 84㎡대 신규 순수전세 65건 가운데 값(영상).
import json, os, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(H, '..', 'rt'); OLD = os.path.join(H, 'old')
def num(s): return float(str(s or '0').replace(',', '') or 0)
def load(d, gu, ym, kind):
    f = os.path.join(d, f'{gu}_{ym}_{kind}.json')
    if not os.path.exists(f): f = os.path.join(RT, f'{gu}_{ym}_{kind}.json')   # 10/11에 받은 뒤 안 바뀐 달은 같은 파일
    if not os.path.exists(f): return []
    x = json.load(open(f, encoding='utf-8')); return x if isinstance(x, list) else x.get('rows', [])
MONTHS = ['202511', '202512'] + [f'2026{m:02d}' for m in range(1, 11)]
APTS = [('고덕아남', '11740', ['아남1', '고덕아남']), ('래미안힐스테이트고덕', '11740', ['래미안힐스테이트고덕', '래미안힐스테이트 고덕']),
        ('고덕그라시움', '11740', ['고덕 그라시움', '고덕그라시움']), ('올림픽파크포레온', '11740', ['올림픽파크포레온']), ('헬리오시티', '11710', ['헬리오시티'])]
def trade(d, gu, names):
    out = []
    for m in MONTHS:
        for r in load(d, gu, m, 'trade'):
            if r.get('cdealType') or r.get('buyerGbn') == '공공기관': continue
            if r.get('aptNm', '').strip() in names and 80 <= num(r['excluUseAr']) < 85: out.append(r)
    return out
def rent(d, gu, names):
    out = []
    for m in MONTHS:
        for r in load(d, gu, m, 'rent'):
            if r.get('aptNm', '').strip() in names and 80 <= num(r['excluUseAr']) < 85 and num(r.get('monthlyRent')) == 0 and r.get('contractType') == '신규': out.append(r)
    return out
res = {}
for nm, gu, names in APTS:
    row = {}
    for tag, d in (('old', OLD), ('new', RT)):
        t = trade(d, gu, names); rr = rent(d, gu, names)
        row[tag] = dict(n=len(t), med=st.median(num(r['dealAmount']) for r in t) / 1e4 if t else None,
                        rn=len(rr), rmed=st.median(num(r['deposit']) for r in rr) / 1e4 if rr else None,
                        oct=[(r['dealDay'], num(r['dealAmount']) / 1e4, r.get('floor')) for r in t if r['dealYear'] == '2026' and r['dealMonth'].lstrip('0') == '10'])
    res[nm] = row
    o, n = row['old'], row['new']
    print(f"{nm}: 영상 값 매매 {o['n']}건 중앙 {o['med']} / 전세 {o['rn']}건 중앙 {o['rmed']}  |  오늘 매매 {n['n']}건 중앙 {n['med']} / 전세 {n['rn']}건 중앙 {n['rmed']} | 10월 매매 {n['oct']}")
json.dump(res, open(os.path.join(H, 'calc_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n[가장 최근 84㎡대 매매 3건]')
for nm, gu, names in APTS:
    t = sorted(trade(RT, gu, names), key=lambda r: (r['dealYear'], r['dealMonth'].zfill(2), r['dealDay'].zfill(2)))[-3:]
    print(nm, [(f"{r['dealYear']}.{r['dealMonth']}.{r['dealDay']}", num(r['dealAmount'])/1e4, r['floor']) for r in t])
print('\n[보증금별 더 필요한 돈 = 매매 가운데 값(오늘) − 보증금]')
for dep in (6.0, 8.0, 9.5, 12.0):
    print(dep, {nm: round(res[nm]['new']['med'] - dep, 2) for nm in res})
