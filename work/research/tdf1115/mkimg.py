# tdf1115 그림 2장 — 숫자는 funetf_out.txt(FunETF 자산비중 26.09.30·NAV 수익률 26.11.13)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#CBD5E1'
# 01: KODEX 4개 주식 비중(왼쪽) · 석 달 수익률(오른쪽)
rows = [('2030', 48.7, -4.54), ('2040', 64.4, -6.40), ('2050', 77.4, -9.03), ('2060', 77.4, -9.01)]
fig, (a, b) = plt.subplots(1, 2, figsize=(9, 5.6), dpi=100, sharey=True)
for i, (n, s, r) in enumerate(rows):
    y = len(rows) - 1 - i; c = ORG if s > 70 else BLU
    a.barh(y, s, color=c, height=0.6); a.text(s + 1.5, y, f'{s}%', va='center', fontproperties=Bs(16), color=c)
    b.barh(y, -r, color=c, height=0.6); b.text(-r + 0.2, y, f'{r:.1f}%', va='center', fontproperties=Bs(16), color=c)
a.set_yticks(range(4)); a.set_yticklabels([f'KODEX TDF{n}' for n, _, _ in rows][::-1], fontproperties=Bs(14), color=INK)
a.set_xlim(0, 100); b.set_xlim(0, 12)
for ax, t in ((a, '주식 비중'), (b, '최근 석 달 수익률')):
    ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
    ax.set_title(t, fontproperties=Bs(18), color=INK, loc='left', pad=10)
fig.suptitle('숫자가 클수록 주식이 많고, 더 많이 빠졌다', fontproperties=Bs(21), color=INK, x=0.02, ha='left')
fig.text(0.01, 0.01, '주식 비중 2026.9.30 · 수익률 2026.8.13~11.13(분배금 재투자 기준가) · 자료: FunETF', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 0.93)); plt.savefig('pkg/img/01.png'); plt.close()
# 02: 같은 2050, 3년 수익률
fig, ax = plt.subplots(figsize=(9, 5.0), dpi=100)
for y, (n, v, cost, c) in enumerate([('KODEX TDF2050', 49.06, 0.43, BLU), ('RISE TDF2050', 56.85, 0.14, ORG)]):
    ax.barh(y, v, color=c, height=0.55); ax.text(v + 1, y, f'{v}%', va='center', fontproperties=Bs(18), color=c)
    ax.text(1.5, y, f'실부담비율 {cost}%', va='center', fontproperties=Bs(13), color='white')
ax.set_yticks([0, 1]); ax.set_yticklabels(['KODEX TDF2050', 'RISE TDF2050'], fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 70); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('같은 2050인데 3년 수익률은 7.8%p 차이', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '3년 수익률 2026.11.13 기준(분배금 재투자 기준가, 비용 빠진 뒤) · 자료: FunETF', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.04, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
