# 미국 기준금리(FRED FEDFUNDS 월평균) vs 한국 예금은행 주담대 금리(ECOS 121Y006 BECBLA0302, 신규취급액) — firemap-write 11/19
import sys, json; sys.path.insert(0, '..'); sys.path.insert(0, '../..')
import apis
kr = {d: float(v) for d, v, _ in apis.ecos(stat='121Y006', cycle='M', start='202112', end='202610', item='BECBLA0302', n=100)}
krb = {d: float(v) for d, v, *_ in apis.ecos(stat='722Y001', cycle='M', start='202112', end='202610', item='0101000', n=100)}
us = {d[:7].replace('-', ''): float(v) for d, v in apis.fred('FEDFUNDS', n=70)}
json.dump({'kr_mortgage': kr, 'kr_base': krb, 'us_ffr': us}, open('raw/series.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ms = sorted(set(kr) & set(us))
print('월 | 미국 기준금리 | 한국 기준금리 | 한국 주담대(신규)')
for m in ms: print(m, us[m], krb.get(m), kr[m])
def chg(a, b, s): return round(s[b] - s[a], 2)
print('\n2022-02→2023-08 미국', chg('202202', '202308', us), '· 한국 주담대', chg('202202', '202308', kr), '· 한국 기준', chg('202202', '202308', krb))
print('주담대 고점', max(kr.items(), key=lambda x: x[1]), '미국 고점 첫 달', min((m for m in us if us[m] == max(us.values()))))
print('2026-08→2026-10 미국', chg('202608', '202610', us), '· 한국 주담대', chg('202608', '202610', kr) if '202610' in kr else '10월 없음')
