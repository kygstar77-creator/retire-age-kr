# 지식iN 질문 1 답: 서울 84㎡ 안팎 10억원 이하 거래 중 연식 띠 · 신축(≤5년) 중 10억 이하
import json, glob, os, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
def num(s): return float(re.sub(r'[^\d.]', '', str(s) or '0') or 0)
R = []
for f in glob.glob(os.path.join(H, 'raw', '*_2026*.json')):
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('cdealType'): continue
        by = int(num(r.get('buildYear')) or 0); a = num(r.get('excluUseAr'))
        if by and 80 <= a <= 86: R.append((2026 - by, num(r.get('dealAmount')) / 1e4))
le = [x for x in R if x[1] <= 10]
print('84㎡ 안팎 10억 이하', len(le), '/', len(R))
print('그중 5년 이내', sum(1 for a, p in le if a <= 5), '· 10년 이내', sum(1 for a, p in le if a <= 10), '· 21년 이상', sum(1 for a, p in le if a >= 21))
n5 = [p for a, p in R if a <= 5]
print('신축(≤5년) 153건 중 10억 이하', sum(1 for p in n5 if p <= 10))
