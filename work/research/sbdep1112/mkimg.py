# sbdep1112 그림 2장 — 01 한 달 새 1년 기본금리 바꾼 저축은행(올림·그대로·내림) · 02 기간별 중간값 은행 vs 저축은행 (calc_out.txt 값)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, ORG, INK, SUBC, GR = '#1D4ED8', '#EA580C', '#111827', '#6B7280', '#CBD5E1'
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
lab = ['올림', '그대로', '내림']; val = [51, 20, 7]; col = [ORG, GR, SUBC]
ax.barh([2, 1, 0], val, color=col, height=0.55)
for i, (l, v) in enumerate(zip(lab, val)):
    ax.text(-1, 2 - i, l, ha='right', va='center', fontproperties=Bs(20), color=INK)
    ax.text(v + 1, 2 - i, f'{v}곳', va='center', fontproperties=Bs(22), color=ORG if i == 0 else INK)
ax.set_xlim(-12, 62); ax.set_ylim(-0.7, 2.7); ax.axis('off')
fig.text(0.05, 0.9, '한 달 새 1년 기본금리를 올린 저축은행', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.84, '두 번 다 공시된 78곳 · 4% 이상 21곳 → 44곳', fontproperties=Bs(15), color=SUBC)
fig.text(0.05, 0.02, '금융감독원 금융상품통합비교공시 정기예금 12개월 · 회사별 가장 높은 기본금리 · 10월 17일 vs 11월 12일 조회', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.78, bottom=0.1)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
terms = ['6개월', '1년', '2년', '3년']; bank = [3.4, 3.6, 2.985, 2.725]; sb = [3.3, 4.0, 2.95, 3.0]
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
def P(v): return str(Decimal(str(v)).quantize(Decimal('0.01'), ROUND_HALF_UP)) + '%'
x = np.arange(4); w = 0.36
ax.bar(x - w/2, bank, w, color=GR, label='은행 18곳'); ax.bar(x + w/2, sb, w, color=BLUE, label='저축은행 79곳')
for i in range(4):
    ax.text(x[i] - w/2, bank[i] + 0.05, P(bank[i]), ha='center', fontproperties=Bs(14), color=SUBC)
    ax.text(x[i] + w/2, sb[i] + 0.05, P(sb[i]), ha='center', fontproperties=Bs(14), color=BLUE)
ax.set_xticks(x); ax.set_xticklabels(terms, fontproperties=Bs(17)); ax.set_ylim(0, 4.6); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(prop=Bs(14), frameon=False, loc='upper right')
fig.text(0.05, 0.92, '1년은 저축은행, 6개월은 은행이 조금 높다', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.02, '금융감독원 금융상품통합비교공시 11월 12일 조회 · 회사별 가장 높은 기본금리의 중간값(우대 조건 뺌)', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.85, bottom=0.12, left=0.05, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
