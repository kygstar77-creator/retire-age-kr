"""E-2 테슬라 원자료 받기 (2026-10-01): SEC companyfacts·submissions. 값은 원본 그대로 raw/에."""
import json, urllib.request, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
UA = {'User-Agent': 'firemap research retireage.kr@gmail.com'}
for name, url in (('tsla_facts.json', 'https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json'),
                  ('tsla_submissions.json', 'https://data.sec.gov/submissions/CIK0001318605.json')):
    b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
    open(os.path.join(R, name), 'wb').write(b); print(name, len(b))
