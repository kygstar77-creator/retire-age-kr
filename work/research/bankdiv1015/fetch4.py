# DART 2026 현금·현물배당결정 공시 목록 + 본문(주당 배당금)
import json, sys, urllib.request, re
sys.path.insert(0, '../../')
import apis
key = apis.key('DART')
cc = json.load(open('src/dart_alot2025.json', encoding='utf-8'))['corp']
H = {'User-Agent': 'Mozilla/5.0'}
out = {}
for n, c in cc.items():
    j = json.load(urllib.request.urlopen(f'https://opendart.fss.or.kr/api/list.json?crtfc_key={key}&corp_code={c}&bgn_de=20260101&end_de=20261015&page_count=100&pblntf_ty=I', timeout=30))
    rows = [r for r in j.get('list', []) if '배당' in r['report_nm']]
    out[n] = rows
    for r in rows: print(n, r['rcept_dt'], r['report_nm'], r['rcept_no'])
json.dump(out, open('src/dart_div2026_list.json', 'w', encoding='utf-8'), ensure_ascii=False)
