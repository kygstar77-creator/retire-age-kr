# cpi1015 계산 — FRED(BLS CPI-U) 원자료만. 전년비는 계절조정 안 한 지수(NSA), 전월비는 계절조정 지수(SA) — BLS 발표 관행
import sys, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
S = {'전체':'CPIAUCNS','근원':'CPILFENS','에너지':'CPIENGNS','식품':'CPIUFDNS','주거':'CUUR0000SAH1','휘발유':'CUUR0000SETB01'}
SA = {'전체':'CPIAUCSL','근원':'CPILFESL','에너지':'CPIENGSL','휘발유':'CUSR0000SETB01'}
raw = {}
def get(s): d = dict(apis.fred(s, 30)); raw[s] = d; return d
yoy = {}
for k, s in S.items():
    d = get(s); yoy[k] = {}
    for m in range(1, 10):
        a, b = d.get(f'2026-{m:02d}-01'), d.get(f'2025-{m:02d}-01')
        if a and b: yoy[k][m] = round((float(a)/float(b)-1)*100, 2)
    print(k, s, {m: v for m, v in yoy[k].items()})
for k, s in SA.items():
    d = get(s); a, b = float(d['2026-09-01']), float(d['2026-08-01'])
    print('전월비', k, s, round((a/b-1)*100, 2))
json.dump(raw, open('fred_raw.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
