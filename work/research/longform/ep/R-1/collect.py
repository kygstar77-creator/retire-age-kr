# R-1 원자료 모으기: 한국은행 ECOS(기준금리·신규 정기예금 1년 금리·CPI) + 금감원 금융상품통합비교공시(12개월 정기예금)
import sys, json, os
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw'); os.makedirs(D, exist_ok=True)
out = {}
k = apis.key('ecos')
def ser(stat, item, start, end, cyc='M'):
    d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/200/{stat}/{cyc}/{start}/{end}/{item}')
    return [(r['TIME'], r['DATA_VALUE']) for r in d.get('StatisticSearch', {}).get('row', [])]
out['기준금리_D'] = ser('722Y001', '0101000', '20220101', '20261003', 'D')
out['정기예금1년_신규_M'] = ser('121Y002', 'BEABAA2118', '202001', '202609')
out['정기예금_신규_M'] = ser('121Y002', 'BEABAA211', '202001', '202609')
out['CPI_M'] = ser('901Y009', '0', '202401', '202609')
for g, code in [('은행', '020000'), ('저축은행', '030300')]:
    rows = []
    for p in range(1, 10):
        r = apis.finlife('deposit', code, p)
        if not r: break
        rows += r
    rows = [x for x in rows if str(x['기간']) == '12']
    out[f'finlife_예금12개월_{g}'] = rows
json.dump(out, open(os.path.join(D, 'collect_20261003.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
b = out['기준금리_D']; chg = [b[0]] + [b[i] for i in range(1, len(b)) if b[i][1] != b[i-1][1]]
print('기준금리 변경:', chg)
print('정기예금1년 신규:', out['정기예금1년_신규_M'][-15:])
print('정기예금1년 2020~ 최고:', max(out['정기예금1년_신규_M'], key=lambda x: float(x[1])))
c = dict(out['CPI_M']); ks = sorted(c); last = ks[-1]; prev = str(int(last[:4]) - 1) + last[4:]
print('CPI', last, c[last], prev, c.get(prev), 'yoy%', round((float(c[last]) / float(c[prev]) - 1) * 100, 2))
for g in ['은행', '저축은행']:
    rs = sorted(out[f'finlife_예금12개월_{g}'], key=lambda x: -(x['금리'] or 0))
    print(f'== {g} 12개월 {len(rs)}줄 공시월', {x["공시월"] for x in rs})
    for x in rs[:8]: print('  기본', x['금리'], '최고', x['최고금리'], x['은행'], x['상품'])
    bs = sorted(x['금리'] for x in rs if x['금리']); print('  기본금리 중앙', bs[len(bs)//2], '최저', bs[0], '최고', bs[-1])
