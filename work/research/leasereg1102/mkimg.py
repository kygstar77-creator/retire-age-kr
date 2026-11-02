# leasereg1102 그림 2장 — 날짜는 판결문(대법원 2024다326398), 비용은 생활법령 백문백답(2026-09-15 기준) · 숫자는 calc.py
import os, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, RED = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#B91C1C'
# 01 판결 사건 날짜 줄
s = D.date(2019, 3, 12)
ev = [(D.date(2019, 3, 12), '신청', INK), (D.date(2019, 3, 20), '법원 결정', INK),
      (D.date(2019, 4, 5), '세입자 이사', RED), (D.date(2019, 4, 8), '등기 완료', ORG)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
ax.plot([0, 27], [0, 0], color=GR, lw=4, zorder=1)
ax.plot([24, 27], [0, 0], color=RED, lw=10, zorder=2, solid_capstyle='butt')
for k, (d, lab, c) in enumerate(ev):
    x = (d - s).days
    ax.scatter([x], [0], s=260, color=c, zorder=3)
    up = 1 if k % 2 == 0 else -1
    ax.text(x, 0.42 * up, f'{d.month}월 {d.day}일', ha='center', va='center', fontproperties=Bs(17), color=c)
    ax.text(x, 0.72 * up, lab, ha='center', va='center', fontsize=15, color=c)
ax.text(25.5, -1.12, '이 사흘은\n대항력 없음', ha='center', va='center', fontsize=13, color=RED, linespacing=1.3)
ax.set_xlim(-3, 30); ax.set_ylim(-1.4, 1.2); ax.axis('off')
fig.text(0.05, 0.9, '신청부터 등기까지 27일 (2019년 사건)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.03, '대법원 2025. 4. 15. 선고 2024다326398 판결문의 날짜', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 신청 비용 43,400원
rows = [('송달료 (5,200원 × 6번)', 31200), ('등록면허세', 7200), ('등기수입증지', 3000), ('수입인지', 2000)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (lab, v) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, v, color=ORG if i == 0 else GR, height=0.55)
    ax.text(v + 500, y, f'{v:,}원', va='center', fontproperties=Bs(18), color=ORG if i == 0 else SUB)
    ax.text(-600, y, lab, ha='right', va='center', fontsize=15, color=INK)
ax.set_xlim(-17000, 40000); ax.set_ylim(-0.7, 3.7); ax.axis('off')
fig.text(0.05, 0.9, '신청 비용 합계 43,400원', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.03, '세입자 1명·집주인 1명·집 1채 · 법제처 생활법령정보(2026년 9월 15일 기준) · 집주인에게 청구 가능', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.03, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
