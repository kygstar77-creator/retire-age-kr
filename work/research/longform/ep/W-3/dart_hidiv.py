# W-3: DART 거래소공시(I) 중 보고서명에 '고배당'·'기업가치' 든 것 모으기 (2026-02~04, 2026-07~10)
import json, sys, time, urllib.request
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
K = apis.key('DART'); out = []
def get(u): return json.loads(urllib.request.urlopen(u, timeout=40).read().decode('utf-8'))
for bgn, end in (('20260201', '20260430'), ('20260501', '20260731'), ('20260801', '20261018')):
    p = 1
    while True:
        d = get(f'https://opendart.fss.or.kr/api/list.json?crtfc_key={K}&bgn_de={bgn}&end_de={end}&pblntf_ty=I&page_no={p}&page_count=100')
        L = d.get('list', [])
        for x in L:
            n = x['report_nm']
            if '고배당' in n or '기업가치' in n: out.append({k: x[k] for k in ('corp_name', 'stock_code', 'report_nm', 'rcept_no', 'rcept_dt')})
        tp = int(d.get('total_page', 1) or 1)
        if p >= tp or not L: break
        p += 1; time.sleep(0.15)
    print(bgn, end, 'pages', tp, 'hits', len(out))
json.dump(out, open('raw/dart_hidiv.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
from collections import Counter
print(Counter(x['report_nm'] for x in out).most_common(15))
