# pen600_1102 그림 2장 — 숫자는 calc.py (소득세법 제59조의3① 15%/12%·600/900만원, 지방세특례제한법 제167조의2① 10%)
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
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
def total(p, i, r):
    b = min(min(p, 600) + i, 900); return b * r * 1.1
def won(v):
    m = int(v); c = round((v - m) * 10)
    return f'{m}만 {c}천원' if c else f'{m}만원'
# 01 연금저축 600만원만 vs IRP 300만원 더 — 두 공제율
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
cases = [('총급여 5,500만원 이하\n(공제율 15%)', .15), ('총급여 5,500만원 초과\n(공제율 12%)', .12)]
x = np.arange(2); w = 0.32
for k, (col, nm, irp) in enumerate([(GR, '연금저축 600만원만', 0), (ORG, '+ IRP 새 돈 300만원', 300)]):
    vals = [total(900, irp, r) for _, r in cases]
    ax.bar(x + (k - .5) * w, vals, w, color=col, label=nm)
    for xi, v in zip(x + (k - .5) * w, vals): ax.text(xi, v + 3, won(v), ha='center', fontsize=14, color=INK)
for i, (_, r) in enumerate(cases):
    d = total(900, 300, r) - total(900, 0, r)
    ax.text(i, total(900, 300, r) + 17, f'+{won(d)}', ha='center', fontproperties=Bs(18), color=ORG)
ax.set_xticks(x); ax.set_xticklabels([c[0] for c in cases], fontsize=14); ax.set_yticks([]); ax.set_ylim(0, 195)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=14, loc='upper right')
fig.text(0.05, 0.92, '1년에 줄어드는 세금 (지방소득세 포함)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.02, '낼 세금이 이보다 적으면 그만큼만 줄어요 · 소득세법 제59조의3', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.16, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 넘친 300만원 처리 — 옮기기 vs 새 돈
fig, ax = plt.subplots(figsize=(9, 6.0), dpi=100)
rows = [('연금저축 넘친 300만원을\nIRP로 옮기면', 0.0, GR), ('IRP에 새 돈\n300만원을 넣으면', total(900, 300, .15) - total(900, 0, .15), ORG)]
for i, (lab, v, c) in enumerate(rows):
    y = 1 - i
    ax.barh(y, max(v, 0.6), color=c, height=0.45)
    ax.text(max(v, 0.6) + 1.2, y, '+0원' if v == 0 else f'+{won(v)}', va='center', fontproperties=Bs(24), color=c if v else SUB)
    ax.text(-1.5, y, lab, ha='right', va='center', fontsize=16, color=INK, linespacing=1.4)
ax.set_xlim(-30, 70); ax.set_ylim(-0.7, 1.7); ax.axis('off')
fig.text(0.05, 0.9, '더 줄어드는 세금 (총급여 5,500만원 이하)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.03, '다른 연금계좌에서 옮겨 온 돈은 공제 대상에서 빠져요 · 소득세법 제59조의3①2호', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
