import json, glob, os, statistics as st, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
RT = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\rt'
def num(s): return float(str(s or 0).replace(',', '') or 0)
def load(kind, months):
    rows = []
    for m in months:
        f = os.path.join(RT, f'11470_{m}_{kind}.json')
        if os.path.exists(f):
            d = json.load(open(f, encoding='utf-8')); rows += d if isinstance(d, list) else d.get('rows', [])
    return rows
ms = sorted({os.path.basename(f).split('_')[1] for f in glob.glob(os.path.join(RT, '11470_2*_trade.json'))})
print('months', ms[0], ms[-1], len(ms))
cur = ms[-12:]; prev = ms[-24:-12]
def clean(rows): return [r for r in rows if r.get('umdNm') == '목동' and not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
T = clean(load('trade', cur)); P = clean(load('trade', prev))
print('목동 1년 거래', len(T), '그 전 1년', len(P), '기간', cur[0], cur[-1])
by = collections.defaultdict(list)
for r in T: by[r['aptNm']].append(r)
byp = collections.defaultdict(list)
for r in P: byp[r['aptNm']].append(r)
out = []
for a, rs in sorted(by.items(), key=lambda x: -len(x[1])):
    bands = collections.Counter(int(num(r['excluUseAr'])//5*5) for r in rs)
    b, n = bands.most_common(1)[0]
    sel = [r for r in rs if int(num(r['excluUseAr'])//5*5) == b]
    med = st.median(num(r['dealAmount']) for r in sel)
    selp = [r for r in byp.get(a, []) if int(num(r['excluUseAr'])//5*5) == b]
    medp = st.median(num(r['dealAmount']) for r in selp) if len(selp) >= 3 else None
    yb = rs[0].get('buildYear')
    last = max(rs, key=lambda r: (r['dealYear'], r['dealMonth'].zfill(2), r['dealDay'].zfill(2)))
    o = dict(apt=a, n=len(rs), build=yb, band=b, band_n=len(sel), area=round(st.median(num(r['excluUseAr']) for r in sel),2), med=med, prev_med=medp, prev_n=len(selp),
             chg=round((med/medp-1)*100,1) if medp else None, last=f"{last['dealYear']}.{last['dealMonth']}.{last['dealDay']} {last['floor']}층 {num(last['dealAmount'])/1e4:.2f}억 {last['excluUseAr']}㎡")
    out.append(o); print(o)
json.dump(out, open('apt_stats.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
mon = collections.Counter(r['dealYear']+r['dealMonth'].zfill(2) for r in T); print(sorted(mon.items()))
