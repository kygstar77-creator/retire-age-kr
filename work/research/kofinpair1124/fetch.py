# kofinpair1124 — 국내 고배당 ETF 10종 업종 비중: 네이버 증권 etfAnalysis + FunETF 업종별 표 (2026-11-23 firemap-write 받음)
import sys, os, re, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
from isin import isin
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
CODES = ['161510', '0105E0', '279530', '315960', '266160', '210780', '0139P0', '322410', '104530', '0153K0']
for c in CODES:
    i = isin(c)
    p = os.path.join(R, f'funetf_{c}.html')
    subprocess.run(['curl', '-s', '-m', '30', '-A', 'Mozilla/5.0', f'https://www.funetf.co.kr/product/etf/view/{i}', '-o', p])
    h = open(p, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<!-- s: 업종별 -->(.*?)<!-- e: 업종별 -->', h, re.S)
    rows = []
    if m:
        t = re.sub(r'<[^>]+>', '|', m.group(1)); t = re.sub(r'\s+', ' ', t)
        rows = [x.strip() for x in t.split('|') if x.strip()]
    print(c, i, rows[:40])
