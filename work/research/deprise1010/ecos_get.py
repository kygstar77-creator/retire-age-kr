# deprise1010 ECOS 받기: 기준금리·정기예금(1년) 신규취급 월별·산금채1년·국고채1년·CD91 일별
import sys, json; sys.path.insert(0, '../..'); sys.stdout.reconfigure(encoding='utf-8')
import apis
out = {}
out['base_D'] = apis.ecos('722Y001', 'D', '20250101', '20261010', '0101000', 1000)
out['dep1y_M'] = apis.ecos('121Y002', 'M', '202501', '202608', 'BEABAA2118', 100)
out['dep_M'] = apis.ecos('121Y002', 'M', '202501', '202608', 'BEABAA211', 100)
for c, n in (('010260000', 'kdb1y'), ('010190000', 'ktb1y'), ('010502000', 'cd91'), ('010200000', 'ktb3y')):
    out[n + '_D'] = apis.ecos('817Y002', 'D', '20250101', '20261010', c, 1000)
json.dump(out, open('ecos_1010.json', 'w', encoding='utf-8'), ensure_ascii=False)
b = out['base_D']; print('base', b[0], [x for i, x in enumerate(b) if i and x[1] != b[i-1][1]], b[-1])
print('dep1y', out['dep1y_M']); print('dep', out['dep_M'])
for n in ('kdb1y', 'ktb1y', 'cd91', 'ktb3y'):
    s = out[n + '_D']; print(n, len(s), s[-1], [x for x in s if x[0][-2:] in ('01',) or x[0] >= '20260901'][-30:])
