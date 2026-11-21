# 야후 ^GSPC(1927~)·^NDX(1985~)·^SP500TR(1988~) 일별 받기 (2026-11-21 firemap-write-b)
import urllib.request, sys
H = {'User-Agent': 'Mozilla/5.0'}
for n, t in [('gspc', '%5EGSPC'), ('ndx', '%5ENDX'), ('sp500tr', '%5ESP500TR'), ('ixic', '%5EIXIC')]:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=-1400000000&period2=1800000000&interval=1d'
    d = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read()
    open(f'raw/{n}_20261121.json', 'wb').write(d); print(n, len(d))
