# 10/21 아웃라이어 2,186편 중 돈 제목 규칙(patterns.py MONEY)에 안 걸린 편 → nonmoney_1021.csv
import csv, re, sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, '..', 'outlier-1021')
src = open(os.path.join(O, 'patterns.py'), encoding='utf-8').read()
MONEY = re.compile(re.search(r"MONEY = re.compile\(r'(.+?)'\)", src).group(1))
rows = list(csv.DictReader(open(os.path.join(O, 'outliers.csv'), encoding='utf-8-sig')))
nm = [r for r in rows if not MONEY.search(r['title'])]
print('전체', len(rows), '돈 아님', len(nm))
with open(os.path.join(H, 'nonmoney_1021.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(nm)
