# bogeum1104 그림 2장 — 아낌e 30년 금리 계단(raw/hist·rate.html) · 1년 전과 지금 월 상환액(calc.py)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
# 01 달별 금리 계단
ms = ['25.12', '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월\n9일~']
rs = [3.85, 4.10, 4.25, 4.25, 4.55, 4.80, 4.80, 5.10, 5.10, 5.10, 5.10, 5.20]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
x = list(range(len(ms)))
ax.step(x, rs, where='post', color=INK, lw=2.2)
ax.plot(x, rs, 'o', color=GR, ms=5)
ax.plot([x[-1]], [rs[-1]], 'o', color=ORG, ms=11)
up = {1: '+0.25', 2: '+0.15', 4: '+0.30', 5: '+0.25', 7: '+0.30', 11: '+0.10'}
for i, t in up.items():
    ax.text(i, rs[i] + 0.07, t, ha='center', fontproperties=Bs(13), color=ORG)
ax.text(0, rs[0] - 0.16, '3.85%', ha='center', fontproperties=Bs(16), color=INK)
ax.text(x[-1], rs[-1] - 0.2, '5.20%', ha='center', fontproperties=Bs(18), color=ORG)
ax.set_xticks(x); ax.set_xticklabels(ms, fontsize=12, color=SUB)
ax.set_ylim(3.5, 5.6); ax.set_yticks([]); 
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
fig.text(0.05, 0.9, '아낌e-보금자리론 30년 금리, 올해만 여섯 번 인상', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.84, '주황 숫자 = 그달 오른 폭(%포인트) · 내린 달은 없음', fontsize=14, color=SUB)
fig.text(0.05, 0.02, '한국주택금융공사 금리안내 2025년 12월~2026년 11월(11월 4일 조회)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.12, left=0.05, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 1년 전과 지금 월 상환액(30년, 원리금균등)
rows = [('2억원', 94, 110, '+16만원'), ('3억원', 141, 165, '+24만원'), ('3억 6천만원', 169, 198, '+29만원')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100); y = 3
for lab, a, b, t in rows:
    ax.text(-8, y, lab, ha='right', va='center', fontproperties=Bs(18), color=INK)
    ax.barh(y + 0.18, a, color=GR, height=0.32); ax.text(a + 2, y + 0.18, f'약 {a}만원', va='center', fontsize=14, color=SUB)
    ax.barh(y - 0.18, b, color=ORG, height=0.32); ax.text(b + 2, y - 0.18, f'약 {b}만원  {t}', va='center', fontproperties=Bs(15), color=ORG)
    y -= 1
ax.set_xlim(-70, 290); ax.set_ylim(0.4, 3.6); ax.axis('off')
fig.text(0.05, 0.9, '30년 만기로 빌리면 매달 내는 돈', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.84, '회색 = 작년 12월(3.85%) · 주황 = 11월 9일부터(5.20%)', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '주택금융공사 아낌e 30년 금리로 원리금균등 직접 계산 · 실제 대출 조건에 따라 다름', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.03, right=0.97); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
