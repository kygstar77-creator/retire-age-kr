# p3pair1111 그림 2장 — 숫자는 calc_out.txt(P-3 calc.py와 같은 식, 재산 0 지역가입자)
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
# 01 월 연금별 한 달 보험료(2026년 요율) — 67,926 · 69,146 · 73,213 · 81,348원
rows = [('월 166만원', 0.0, LG, '0원'), ('월 167만원', 6.8, ORG, '약 6.8만원'), ('월 170만원', 6.9, BLU, '약 6.9만원'),
        ('월 180만원', 7.3, BLU, '약 7.3만원'), ('월 200만원', 8.1, BLU, '약 8.1만원')]
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
for i, (n, v, c, lab) in enumerate(rows):
    ax.bar(i, max(v, 0.08), color=c, width=0.6)
    ax.text(i, v + 0.25, lab, ha='center', fontproperties=Bs(16), color=ORG if c == ORG else INK)
ax.set_xticks(range(5)); ax.set_xticklabels([r[0] for r in rows], fontproperties=Bs(14))
ax.set_ylim(0, 10); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='x', length=0)
fig.text(0.05, 0.93, '국민연금 월 얼마면 건보료 한 달 얼마', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.885, '피부양자에서 빠진 뒤 지역가입자 보험료 · 건강보험+장기요양 · 재산 없는 경우', fontsize=12.5, color=SUB)
fig.text(0.05, 0.02, '시행규칙 제44조(연금 50% 반영) · 보험료율 7.19% · 장기요양 13.14%(2026년) · 직접 계산', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 2027년 — 세 칸
fig = plt.figure(figsize=(9, 5.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.88, '2027년에 바뀌는 것, 그대로인 것', fontproperties=Bs(22), color=INK)
L = [('건강보험료율', '7.19% 그대로 (2026년 9월 8일 결정)'),
     ('장기요양보험료', '건강보험료의 13.14% → 13.90%'),
     ('월 167만원이면', '한 달 6만 8,382원 (456원 더)')]
for i, (a, b) in enumerate(L):
    y = 0.68 - i * 0.22
    fig.patches.append(plt.Rectangle((0.05, y - 0.07), 0.9, 0.17, transform=fig.transFigure, color='#F3F4F6', zorder=0))
    fig.text(0.08, y + 0.035, a, fontproperties=Bs(15), color=SUB)
    fig.text(0.08, y - 0.035, b, fontproperties=Bs(18), color=ORG if i == 2 else INK)
fig.text(0.05, 0.03, '보건복지부 발표(2026.9.8 · 2026.10.30) · 재산 없는 지역가입자 직접 계산', fontsize=11.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
