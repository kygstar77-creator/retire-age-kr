# hmcdiv1104 그림 2장 — 이번 배당 날짜(DART 10.29)·1천만원 넘는 데 드는 돈(calc.py)
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
# 01 2026년에 받는 1주당 배당
# 01 이번 배당 날짜
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
pts = [(0.5, '11월 26일(목)', '이날까지 사야'), (2.0, '11월 30일(월)', '주주명부 기준일'), (3.5, '12월 30일', '지급 예정')]
ax.plot([0.3, 3.7], [1, 1], color=GR, lw=3)
for x, d, s in pts:
    hot = x == 0.5
    ax.scatter([x], [1], s=420, color=ORG if hot else INK, zorder=3)
    ax.text(x, 1.45, d, ha='center', fontproperties=Bs(20), color=ORG if hot else INK)
    ax.text(x, 0.45, s, ha='center', fontsize=16, color=SUB)
ax.set_xlim(0, 4); ax.set_ylim(0, 2.2); ax.axis('off')
fig.text(0.05, 0.88, '현대차 3분기 배당 1주당 2,500원', fontproperties=Bs(24), color=INK)
fig.text(0.05, 0.80, '100주면 세금 15.4% 떼고 21만 1,500원', fontsize=17, color=SUB)
fig.text(0.05, 0.03, '금융감독원 DART 현대자동차 현금·현물배당결정(2026.10.29) · 결제는 산 날 포함 3영업일째(한국거래소 업무규정 제7조)', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.78, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 1년 배당 1천만원 넘는 데 드는 돈
rows = [('보통주 1,001주', 2.84, GR), ('현대차2우B 991주', 1.50, ORG)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (lab, v, c) in enumerate(rows):
    y = 1 - i
    ax.barh(y, v, color=c, height=0.5)
    ax.text(-0.05, y, lab, ha='right', va='center', fontproperties=Bs(17), color=INK)
    ax.text(v + 0.06, y, f'약 {"2억 8,400만원" if i == 0 else "1억 5,000만원"}', va='center', fontproperties=Bs(18), color=c if i else SUB)
ax.set_xlim(-1.9, 4.2); ax.set_ylim(-0.7, 1.7); ax.axis('off')
fig.text(0.05, 0.88, '1년 배당 1천만원을 넘기는 데 드는 돈', fontproperties=Bs(24), color=INK)
fig.text(0.05, 0.80, '우선주는 보통주의 절반 수준', fontsize=17, color=SUB)
fig.text(0.05, 0.03, '2026년 1주당 배당 보통 1만원·우선 1만 100원(DART 공시 4건) · 2026년 11월 4일 종가 28만 3,500원·15만 1,800원(야후 파이낸스)', fontsize=10, color='#6B7280')
fig.subplots_adjust(top=0.78, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
