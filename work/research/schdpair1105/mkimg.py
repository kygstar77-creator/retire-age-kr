# schdpair1105 그림 2장 — 배당 ETF 6개 최근 1년·10년 성장률(calc_out) · SCHD 분기 배당 올해 vs 작년(슈왑 표)
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
# 01 최근 1년 성장률 막대(10년 평균은 글자로)
rows = [('DVY', 10.3, 7.1), ('NOBL', 9.2, 8.7), ('DGRO', 8.1, None), ('VYM', 4.5, 5.6), ('VIG', 2.7, 7.8), ('SCHD', 2.0, 10.8)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100); y = 6
for t, a, b in rows:
    c = ORG if t == 'SCHD' else GR
    ax.text(-0.4, y, t, ha='right', va='center', fontproperties=Bs(18), color=INK)
    ax.barh(y, a, color=c, height=0.6)
    ax.text(a + 0.25, y, f'{a:.1f}%', va='center', fontproperties=Bs(18), color=ORG if t == 'SCHD' else INK)
    ax.text(14.6, y, f'{b:.1f}%' if b is not None else '—', va='center', ha='right', fontsize=15, color=SUB); y -= 1
ax.text(14.6, 6.75, '10년 평균', ha='right', fontproperties=Bs(14), color=SUB)
ax.set_xlim(-3, 15); ax.set_ylim(0.4, 7.1); ax.axis('off')
fig.text(0.05, 0.9, '최근 12개월 배당이 1년 전보다 늘어난 비율', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.83, '1주당 배당 합 · 11월 4일까지 12개월 vs 1년 전 같은 12개월', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '야후 파이낸스 배당 기록(11월 4일 조회, 분할 반영) · SCHD는 슈왑 원문과 대조 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.03, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 SCHD 분기 배당 올해 vs 작년
q = ['12월', '3월', '6월', '9월']; now = [0.2782, 0.2569, 0.2525, 0.2665]; pre = [0.2645, 0.2488, 0.2602, 0.2604]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
x = range(4)
ax.bar([i - 0.2 for i in x], pre, width=0.38, color=GR, label='1년 전')
ax.bar([i + 0.2 for i in x], now, width=0.38, color=[ORG if n < p else INK for n, p in zip(now, pre)], label='최근')
for i, (n, p) in enumerate(zip(now, pre)):
    ax.text(i - 0.2, p + 0.002, f'{p:.4f}', ha='center', fontsize=12, color=SUB)
    ax.text(i + 0.2, n + 0.002, f'{n:.4f}', ha='center', fontproperties=Bs(13), color=ORG if n < p else INK)
ax.set_xticks(list(x)); ax.set_xticklabels(q, fontproperties=Bs(16)); ax.set_ylim(0.22, 0.29); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, 'SCHD 1주당 분기 배당 (달러)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.86, '회색 = 1년 전 · 검정 = 최근(2025년 12월~2026년 9월) · 주황 = 작년보다 적음', fontsize=14, color=SUB)
fig.text(0.05, 0.02, '슈왑 SCHD 배당 기록(Distributions) · 주식 분할 뒤 금액', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.15, left=0.05, right=0.97); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
