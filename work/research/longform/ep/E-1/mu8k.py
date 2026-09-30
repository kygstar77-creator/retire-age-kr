"""마이크론 실적 8-K(항목 2.02) 원문 받기 — 사용: py -3.12 mu8k.py <accession> [--show]
EX-99.1 보도자료를 raw/mu_8k_<acc>.htm·.txt로 저장하고, 매출·이익·사업부·전망 문단을 뽑아 보여 준다."""
import sys, re, html, json, urllib.request, os
UA = {'User-Agent': 'firemap research kygstar77@gmail.com'}
acc = sys.argv[1]; nodash = acc.replace('-', '')
base = f'https://www.sec.gov/Archives/edgar/data/723125/{nodash}/'
idx = json.load(urllib.request.urlopen(urllib.request.Request(base + 'index.json', headers=UA)))
names = [i['name'] for i in idx['directory']['item']]
ex = [n for n in names if re.search(r'ex99-?1|ex991|ex-99', n, re.I) and n.endswith('.htm')] or [n for n in names if n.endswith('.htm')]
print('files', names); print('ex99.1', ex[0])
raw = urllib.request.urlopen(urllib.request.Request(base + ex[0], headers=UA)).read().decode('utf-8', 'ignore')
os.makedirs('raw', exist_ok=True)
open(f'raw/mu_8k_{acc}.htm', 'w', encoding='utf-8').write(raw)
t = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw)))
open(f'raw/mu_8k_{acc}.txt', 'w', encoding='utf-8').write(t)
for pat in [r'Revenue', r'Gross margin', r'Operating income', r'Business Unit|Cloud Memory|Mobile and Client|Automotive', r'Guidance|guidance', r'dividend', r'HBM']:
    for m in list(re.finditer(pat, t))[:2]:
        print('##', pat, '::', t[max(0, m.start()-200):m.start()+600]); print()
