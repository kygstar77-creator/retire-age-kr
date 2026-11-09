# ltdeduct1110 그림 2장 — 01 해마다 빼 주는 비율(법안 표2·상세본 p.57), 02 8억→20억 파는 해별 세금(calc.py)
import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
import calc
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, GR, SUBC = '#1D4ED8', '#111827', '#94A3B8', '#6B7280'
years = ['2027년까지', '2028년', '2029년부터']
# 01 빼 주는 비율
r10 = [80, 80, 80]; r2 = [48, 32, 16]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
x = np.arange(3); w = 0.36
ax.bar(x - w/2, r10, w, color=GR, label='10년 산 집')
ax.bar(x + w/2, r2, w, color=BLUE, label='2년만 산 집')
for xi, a, b in zip(x, r10, r2):
    ax.text(xi - w/2, a + 1.5, f'{a}%', ha='center', fontsize=16, color=INK)
    ax.text(xi + w/2, b + 1.5, f'{b}%', ha='center', fontproperties=Bs(18), color=BLUE)
ax.set_xticks(x); ax.set_xticklabels(years, fontproperties=Bs(16)); ax.set_yticks([]); ax.set_ylim(0, 108)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=14, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.04))
fig.text(0.05, 0.92, '10년 갖고 있던 1주택, 빼 주는 비율', fontproperties=Bs(23), color=INK)
fig.text(0.05, 0.02, '정부 소득세법 개정안(2221042) 표2 · 재정경제부 문답자료 37쪽 · 국회 심사 중', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 세금
yr = [(2026, '현행', '지금'), (2027, '현행', '2027년'), (2028, '2028', '2028년'), (2029, '2029', '2029년')]
t10 = [calc.case(8e8, 20e8, 10, 10, r, y)['total'] for y, r, _ in yr]
t2 = [calc.case(8e8, 20e8, 10, 2, r, y)['total'] for y, r, _ in yr]
def won(v):
    m = round(v / 1e6) * 100  # 만원 단위, 백만 자리 반올림
    return f'약 {m//10000}억 {m%10000:,}만원' if m >= 10000 else f'약 {m:,}만원'
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
x = np.arange(4); w = 0.36
ax.bar(x - w/2, t10, w, color=GR, label='10년 산 집')
ax.bar(x + w/2, t2, w, color=BLUE, label='2년만 산 집')
for xi, a, b in zip(x, t10, t2):
    ax.text(xi - w/2, a + 2e6, won(a).replace('약 ', ''), ha='center', fontsize=11, color=INK)
    ax.text(xi + w/2, b + 2e6, won(b).replace('약 ', ''), ha='center', fontproperties=Bs(12), color=BLUE)
ax.set_xticks(x); ax.set_xticklabels([l for _, _, l in yr], fontproperties=Bs(16)); ax.set_yticks([]); ax.set_ylim(0, 1.75e8)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=14, loc='upper left')
fig.text(0.05, 0.92, '8억에 사서 20억에 팔 때 양도세(파는 해별)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.02, '10년 보유·단독명의·지방소득세 포함 · 정부안대로 통과될 때 · 재정경제부 계산 예시와 같은 방식으로 계산', fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print([won(v) for v in t10], [won(v) for v in t2])
