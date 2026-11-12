# dfopt1112 그림 2장 — 01 위험도별 적립금 비중·1년 수익률 · 02 위험도별 최근 3개월 vs 1년 중앙값 (calc_out.txt·공시 시트2 값)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, ORG, INK, SUBC, GR = '#1D4ED8', '#EA580C', '#111827', '#6B7280', '#CBD5E1'
lab = ['초저위험\n(원리금보장)', '저위험', '중위험', '고위험']
share = [82.4, 8.4, 5.5, 3.6]; r1 = [2.5, 6.56, 9.39, 13.95]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
y = [3, 2, 1, 0]
ax.barh(y, share, color=[BLUE, GR, GR, GR], height=0.55)
for i in range(4):
    ax.text(-2, y[i], lab[i], ha='right', va='center', fontproperties=Bs(17), color=INK)
    ax.text(share[i] + 1.5, y[i], f'돈의 {share[i]}%  ·  1년 {r1[i]}%', va='center', fontproperties=Bs(18), color=ORG if i == 0 else INK)
ax.set_xlim(-30, 130); ax.set_ylim(-0.7, 3.7); ax.axis('off')
fig.text(0.05, 0.9, '디폴트옵션 돈 10원 중 8원은 원리금보장에', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.84, '332개 상품 적립금 55.9조원 · 위험도별 비중과 1년 수익률', fontproperties=Bs(15), color=SUBC)
fig.text(0.05, 0.02, '고용노동부 사전지정운용방법 상품별 비교공시(2026년 9월 30일 기준) · 1년 수익률은 공시의 위험도별 값', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.78, bottom=0.1)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
m3 = [0.84, -2.24, -4.82, -7.16]
x = np.arange(4)
ax.bar(x, m3, 0.55, color=[GR, SUBC, SUBC, ORG])
for i in range(4):
    ax.text(x[i], m3[i] + (0.25 if m3[i] >= 0 else -0.75), f'{m3[i]}%', ha='center', fontproperties=Bs(18), color=ORG if i == 3 else INK)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(x); ax.set_xticklabels(['초저위험', '저위험', '중위험', '고위험'], fontproperties=Bs(17)); ax.set_ylim(-9, 2.5); ax.set_yticks([])
ax.tick_params(axis='x', length=0)
for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '최근 석 달(7~9월), 위험도가 높을수록 더 빠졌다', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.86, '위험도별 상품을 수익률 순서로 세웠을 때 한가운데 상품(중간값)', fontproperties=Bs(15), color=SUBC)
fig.text(0.05, 0.02, '고용노동부 사전지정운용방법 상품별 비교공시(2026년 9월 30일 기준) · 최근 3개월 수익률', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.8, bottom=0.12, left=0.05, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
