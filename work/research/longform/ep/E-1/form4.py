"""마이크론 Form 4(임원·이사 주식 거래) 최근 6개월 원문 → raw/mu_form4/*.xml, form4.json (2026-09-30).
코드 S=공개시장 매도, P=매수, M=옵션 행사, F=세금 원천 징수, A=부여. 10b5-1 표시는 각주에서 찾는다."""
import json, os, sys, time, urllib.request, re, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'raw', 'mu_form4'); os.makedirs(D, exist_ok=True)
UA = {'User-Agent': 'firemap research retireage.kr@gmail.com'}
r = json.load(open(os.path.join(H, 'raw', 'mu_submissions.json'), encoding='utf-8'))['filings']['recent']
rows = []
for i, form in enumerate(r['form']):
    if form != '4' or r['filingDate'][i] < '2026-04-01': continue
    acc = r['accessionNumber'][i]; p = os.path.join(D, acc + '.xml')
    if not os.path.exists(p):
        doc = r['primaryDocument'][i].split('/')[-1]
        u = f"https://www.sec.gov/Archives/edgar/data/723125/{acc.replace('-', '')}/{doc}"
        open(p, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()); time.sleep(0.2)
    t = ET.parse(p).getroot()
    who = t.findtext('.//reportingOwner/reportingOwnerId/rptOwnerName')
    title = t.findtext('.//reportingOwnerRelationship/officerTitle') or ('Director' if t.findtext('.//reportingOwnerRelationship/isDirector') in ('1', 'true') else '')
    plan = '10b5-1' in ET.tostring(t, encoding='unicode')
    for tx in t.findall('.//nonDerivativeTable/nonDerivativeTransaction'):
        rows.append({'filed': r['filingDate'][i], 'acc': acc, 'who': who, 'title': title,
                     'date': tx.findtext('transactionDate/value'), 'code': tx.findtext('transactionCoding/transactionCode'),
                     'shares': float(tx.findtext('transactionAmounts/transactionShares/value') or 0),
                     'price': float(tx.findtext('transactionAmounts/transactionPricePerShare/value') or 0),
                     'ad': tx.findtext('transactionAmounts/transactionAcquiredDisposedCode/value'),
                     'after': float(tx.findtext('postTransactionAmounts/sharesOwnedFollowingTransaction/value') or 0), 'plan10b5_1': plan})
json.dump(rows, open(os.path.join(H, 'form4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import defaultdict
agg = defaultdict(lambda: [0, 0.0])
for x in rows: agg[x['code']][0] += x['shares']; agg[x['code']][1] += x['shares'] * x['price']
print('건수', len(rows)); [print(k, f'{v[0]:,.0f}주', f'${v[1]:,.0f}') for k, v in agg.items()]
for x in rows:
    if x['code'] in ('S', 'P'): print(x['date'], x['who'], x['title'], x['code'], f"{x['shares']:,.0f}", x['price'], '10b5-1' if x['plan10b5_1'] else '')
