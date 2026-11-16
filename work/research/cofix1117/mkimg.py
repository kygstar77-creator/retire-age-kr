# cofix1117 그림 2장 — 숫자는 calc_out.txt(은행연합회 COFIX 월별 공시, 한국은행 ECOS 기준금리)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, GRN, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#059669', '#CBD5E1'
m = ['25.10','11','12','26.1','2','3','4','5','6','7','8','9','10']
new = [2.57,2.81,2.89,2.77,2.82,2.81,2.89,2.90,3.05,3.18,3.18,3.43,3.62]
bal = [2.84,2.83,2.84,2.85,2.85,2.85,2.87,2.89,2.94,3.00,3.05,3.15,3.26]
nbal= [2.48,2.48,2.47,2.48,2.47,2.45,2.49,2.50,2.54,2.65,2.71,2.79,2.93]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for v, c, n in [(new, ORG, '신규취급액'), (bal, BLU, '잔액'), (nbal, GRN, '신잔액')]:
    ax.plot(range(13), v, color=c, lw=3.2, marker='o', ms=5)
    ax.text(12.25, v[-1], f'{n} {v[-1]:.2f}%', va='center', fontproperties=Bs(14), color=c)
    ax.text(-0.25, v[0], f'{v[0]:.2f}', va='center', ha='right', fontproperties=Bs(12), color=c)
ax.set_xticks(range(13)); ax.set_xticklabels(m, fontproperties=Bs(12), color=SUB)
ax.set_xlim(-1.3, 15.6); ax.set_ylim(2.3, 3.8); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.suptitle('1년 새 신규취급액 코픽스만 크게 올랐어요', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.03, '은행연합회 COFIX 월별 공시 · 2025년 10월~2026년 10월(대상월) · 단위 %', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.05, right=0.97, top=0.85, bottom=0.13)
fig.savefig('pkg/img/01.png'); plt.close(fig)
rows = [('신규취급액', 315, 26, ORG), ('잔액', 126, 10, BLU), ('신잔액', 135, 11, GRN)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, y, mo, c) in enumerate(rows):
    ax.bar(i, y, color=c, width=0.55)
    ax.text(i, y + 8, f'1년 약 {y}만원', ha='center', fontproperties=Bs(18), color=INK)
    ax.text(i, y / 2, f'한 달\n약 {mo}만원', ha='center', va='center', fontproperties=Bs(15), color='white')
ax.set_xticks(range(3)); ax.set_xticklabels([r[0] + ' 기준' for r in rows], fontproperties=Bs(16), color=INK)
ax.set_ylim(0, 370); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.suptitle('3억원 대출, 1년 새 늘어난 이자', fontproperties=Bs(24), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.015, '원금·가산금리 그대로, 코픽스 오른 폭만 계산 · 2025년 10월→2026년 10월 · 은행연합회 COFIX', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.06, right=0.96, top=0.85, bottom=0.16)
fig.savefig('pkg/img/02.png'); plt.close(fig)
print('ok')
