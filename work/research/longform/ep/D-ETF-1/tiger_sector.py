import json, csv, re, sys
b = json.load(open('items_KR7466940004.json', encoding='utf-8'))['rtnData']
print('TIGER은행', b[0]['wkdate'], len(b), round(sum(x['stockRate'] for x in b),2))
for x in b: print(' ', x['memItemname'], x['stockRate'])
u = json.load(open('items_KR7458730009.json', encoding='utf-8'))['rtnData']
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
def key(s): s = re.sub(r'[^A-Z0-9 ]', ' ', s.upper()); w = [t for t in s.split() if t not in ('INC','CORP','CO','THE','CORPORATION','COMPANY','LTD','PLC','CLASS','A','B','HOLDINGS','GROUP')]; return w
sec = {}; un = []
for x in u:
    k = key(x['memItemnameEng'] or x['memItemname'])
    if not k or x['memItemgb'] != '2': un.append((x['memItemname'], x['stockRate'])); continue
    best = None
    for r in rows:
        rk = key(r['Name'] or '')
        if rk and rk[0] == k[0] and (len(k) < 2 or len(rk) < 2 or rk[1][:3] == k[1][:3]): best = r; break
    if not best: un.append((x['memItemname'], x['stockRate'])); continue
    sec[best['Sector']] = sec.get(best['Sector'], 0) + x['stockRate']
print('TIGER미국배당', u[0]['wkdate'], len(u), 'sum', round(sum(x['stockRate'] for x in u),2))
for s, v in sorted(sec.items(), key=lambda t: -t[1]): print(' ', s, round(v, 2))
print('unmatched', un)
print('--- check')
for x in u:
    k = key(x['memItemnameEng'] or x['memItemname'])
    for r in rows:
        rk = key(r['Name'] or '')
        if k and rk and rk[0] == k[0] and (len(k) < 2 or len(rk) < 2 or rk[1][:3] == k[1][:3]):
            if r['Sector'] in ('Health Care','Consumer Staples'): print(x['memItemnameEng'], '|', r['Name'], r['Percent of Assets'][:5], x['stockRate'])
            break
