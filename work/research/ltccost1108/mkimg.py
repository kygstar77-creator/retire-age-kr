# ltccost1108 그림 2장 — 숫자는 calc.py(공단 2026.1.1 하루 비용 × 30일 × 20%/12%/8%)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, LG = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#CBD5E1'
day = [('1등급', 93070), ('2등급', 86340), ('3~5등급', 81540)]
rates = [('20% (보통)', .20, ORG), ('12% (40% 깎음)', .12, GR), ('8% (60% 깎음)', .08, LG)]
def man(v): return f'{v/10000:.1f}만'
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
x = np.arange(3); w = 0.26
for k, (nm, r, c) in enumerate(rates):
    vals = [d*30*r for _, d in day]
    ax.bar(x + (k-1)*w, vals, w, color=c, label=nm)
    for xi, v in zip(x + (k-1)*w, vals): ax.text(xi, v + 8000, man(v), ha='center', fontsize=13, color=INK)
ax.set_xticks(x); ax.set_xticklabels([g for g, _ in day], fontproperties=Bs(16)); ax.set_yticks([]); ax.set_ylim(0, 680000)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=14, loc='upper right')
fig.text(0.05, 0.92, '요양원 30일, 본인이 내는 돈 (원)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.02, '식재료비·이미용비·상급침실 비용은 빼고 셈 · 공단 2026.1.1 하루 급여비용(요양보호사 2.1명당 1명 이상)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.14, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 감경이 빠지는 두 경우
fig = plt.figure(figsize=(9, 6.2), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.88, '보험료 감경이 빠지는 두 경우', fontproperties=Bs(24), color=INK)
rows = [('1', '요양원으로 주민등록 주소를 옮긴 지역가입자', '옮긴 달에 이미 감경 중이었으면 그대로'),
        ('2', '자녀 피부양자 → 혼자 지역가입자, 주소는 그 자녀와 같음', '피부양자일 때 이미 감경 중이었으면 그대로')]
for i, (n, a, b) in enumerate(rows):
    y = 0.64 - i*0.3
    from matplotlib.patches import Ellipse; fig.patches.append(Ellipse((0.09, y), 0.07*6.2/9, 0.07, transform=fig.transFigure, color=ORG))
    fig.text(0.09, y, n, ha='center', va='center', fontproperties=Bs(20), color='white')
    fig.text(0.16, y + 0.03, a, fontproperties=Bs(17), color=INK, va='center')
    fig.text(0.16, y - 0.06, '예외: ' + b, fontsize=14, color=SUB, va='center')
fig.text(0.06, 0.1, '바꾸기 전에 공단 1577-1000에 감경이 이어지는지 확인', fontproperties=Bs(16), color=ORG)
fig.text(0.06, 0.03, '장기요양 본인부담금 감경에 관한 고시 제2조의2', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
