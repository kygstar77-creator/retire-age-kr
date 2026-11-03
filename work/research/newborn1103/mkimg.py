# newborn1103 그림 2장 — 8.5천 초과 종료 후 금리 접수 달별 35달(S3)·3억 30년 6년째 월 상환액(calc.py)
import os, re, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
# 01 접수 달별 종료 후 금리(소득 8,500만원 초과)
s = open('raw/after_rate.json', encoding='utf-8').read().strip()
d = json.loads(re.sub(r'^\{arrJson\s*:', '{"arrJson":', s))['arrJson'][::-1]
xs = list(range(len(d))); ys = [float(j['STDRATE']) for j in d]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
ax.plot(xs, ys, color=GR, lw=3)
ax.plot(xs[-1], ys[-1], 'o', color=ORG, ms=12)
ax.text(xs[-1] - 0.6, ys[-1] + 0.1, '2026년 11월 4.77%', ha='right', fontproperties=Bs(18), color=ORG)
i9 = min(xs, key=lambda i: ys[i]); ax.plot(i9, ys[i9], 'o', color=SUB, ms=8)
ax.text(i9, ys[i9] - 0.2, '2024년 9월 3.31%', ha='center', fontsize=14, color=SUB)
for i, j in enumerate(d):
    if j['STD_YEAR_MONTH'].endswith('.01'): ax.text(i, 2.85, j['STD_YEAR_MONTH'][:4] + '년', ha='center', fontsize=13, color=SUB)
ax.set_ylim(2.7, 5.1); ax.set_xlim(-1.5, len(d) + 0.5); ax.axis('off')
fig.text(0.05, 0.9, '6년째 금리는 접수한 달에 정해져요', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.83, '부부 합산 연소득 8,500만원 초과 · 수도권 기준', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '주택도시기금포털 신생아 특례 디딤돌 \'특례금리 적용 종료 후 적용 금리\'(2024.1~2026.11, 11월 3일 조회)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 3억 30년 월 상환액, 처음 5년 → 6년째
rows = [('연소득 7천만원', 1248690, 1354324), ('연소득 1억원', 1297401, 1529185), ('맞벌이 1.6억원', 1458310, 1553818)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
y = 3.0
for lab, a, b in rows:
    ax.text(-30, y + 0.02, lab, ha='right', va='center', fontproperties=Bs(16), color=INK)
    ax.barh(y + 0.3, a / 1e4, color=GR, height=0.45); ax.text(a / 1e4 + 3, y + 0.3, f'처음 5년 {a/1e4:.0f}만원', va='center', fontsize=14, color=SUB)
    ax.barh(y - 0.25, b / 1e4, color=ORG, height=0.45); ax.text(b / 1e4 + 3, y - 0.25, f'6년째 {b/1e4:.0f}만원 (+{(b-a)/1e4:.1f}만)', va='center', fontproperties=Bs(15), color=ORG)
    y -= 1.25
ax.set_xlim(-75, 240); ax.set_ylim(0.1, 3.6); ax.axis('off')
fig.text(0.05, 0.9, '3억원 30년, 6년째 월 상환액', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.83, '11월 접수 · 수도권 · 원리금균등 · 우대금리 뺀 기본 금리', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '주택도시기금포털 신생아 특례·신혼부부 금리표(11월 3일 조회)로 직접 계산', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
