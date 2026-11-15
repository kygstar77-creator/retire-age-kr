# isa1116 그림 2장 — 숫자는 calc_out.txt(금투협 ISA 운용 현황 2026-09-30·금감원 정기예금 공시)
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
# 01: 은행 신탁형 vs 증권 중개형 — 돈이 어디 들어 있나(3칸: 예금·적금 / ETF 등 / 주식·그 밖)
rows = [('은행 신탁형', 88.9, 8.8, 100-88.9-8.8), ('증권사 중개형', 6.3, 51.6, 100-6.3-51.6)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, dep, etf, oth) in enumerate(rows):
    y = 1 - i
    ax.barh(y, dep, color=ORG, height=0.5); ax.barh(y, etf, left=dep, color=BLU, height=0.5); ax.barh(y, oth, left=dep+etf, color=LG, height=0.5)
    ax.text(dep/2 if dep > 15 else 0, y if dep > 15 else y + 0.36, (f'예금·적금'+chr(10)+f'{dep}%' if dep > 15 else f'예금·적금 {dep}%'), ha='center' if dep > 15 else 'left', va='center', fontproperties=Bs(15), color='white' if dep > 15 else ORG)
    if etf > 15: ax.text(dep + etf/2, y, f'ETF 등\n{etf}%', ha='center', va='center', fontproperties=Bs(15), color='white')
ax.text(6.3 + 51.6 + 42.1/2, 0, '주식 35.3%\n그 밖 6.8%', ha='center', va='center', fontproperties=Bs(14), color=INK)
ax.set_yticks([1, 0]); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(17), color=INK)
ax.set_xlim(0, 100); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('ISA 안의 돈, 어디에 들어 있나', fontproperties=Bs(24), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.03, '금융투자협회 ISA 운용(편입자산) 현황 · 2026년 9월 말 · 금액 비중', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.2, right=0.96, top=0.82, bottom=0.1)
fig.savefig('pkg/img/01.png'); plt.close(fig)
# 02: 예금 원금별 3년 이자(연 3.285%) vs 한도 200·400만원
per = [('650만원\n(증권사 평균)', 653), ('1,700만원\n(은행 평균)', 1709), ('2,030만원', 2029), ('4,060만원', 4059)]
r = 0.03285
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, a) in enumerate(per):
    v = a * r * 3
    c = ORG if i >= 2 else LG
    ax.bar(i, v, color=c, width=0.55)
    ax.text(i, v + 8, f'약 {v:.0f}만원', ha='center', fontproperties=Bs(16), color=INK)
for lim, lab in [(200, '일반형 한도 200만원'), (400, '서민형 한도 400만원')]:
    ax.axhline(lim, color=BLU, lw=2, ls='--'); ax.text(-0.45, lim + 6, lab, fontproperties=Bs(13), color=BLU)
fig.text(0.5, 0.075, '예금에 넣은 원금', ha='center', fontproperties=Bs(12), color=SUB)
ax.set_xticks(range(4)); ax.set_xticklabels([p[0] for p in per], fontproperties=Bs(14), color=INK)
ax.set_ylim(0, 470); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.suptitle('예금에 3년 맡기면 이자는 얼마', fontproperties=Bs(24), color=INK, x=0.04, ha='left', y=0.97)
fig.text(0.04, 0.015, '정기예금 1년 기본금리 중간값 연 3.285%(금감원 공시 40개 상품, 2026년 10월) · 이자는 해마다 꺼내 쓴다고 봄', fontproperties=Bs(10.5), color=SUB)
plt.subplots_adjust(left=0.06, right=0.96, top=0.85, bottom=0.25)
fig.savefig('pkg/img/02.png'); plt.close(fig)
print('ok')
