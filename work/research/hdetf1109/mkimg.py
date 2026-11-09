# hdetf1109 그림 2장 — 숫자는 calc_out.txt(국세청 기본세율표·조특법 104조의27 세율·소득세법 제62조)
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
# 01 분배금 3천만원일 때 ETF가 더 내는 소득세(만원) — 다른 소득 과세표준별
rows = [('다른 소득 없음', -60), ('다른 소득 과세표준 3천만원', -50), ('다른 소득 과세표준 6천만원', 40), ('다른 소득 과세표준 1억원', 150)]
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
for i, (n, v) in enumerate(rows[::-1]):
    c = ORG if v > 0 else BLU
    ax.barh(i, v, color=c, height=0.55)
    ax.text((v if v > 0 else 0) + 6, i, (f'ETF가 {v}만원 더' if v > 0 else f'ETF가 {-v}만원 덜'), va='center',
            ha='left', fontproperties=Bs(15), color=c)
ax.axvline(0, color=SUB, lw=1)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]], fontproperties=Bs(13.5))
ax.set_xlim(-160, 260); ax.set_xticks([])
for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.04, 0.93, '1년 배당 3천만원, ETF로 받으면 세금이 더 많을까', fontproperties=Bs(20), color=INK)
fig.text(0.04, 0.885, '고배당기업 주식을 직접 갖고 분리과세를 신청한 경우와 비교 · 소득세만(지방소득세 10% 따로)', fontsize=12, color=SUB)
fig.text(0.04, 0.02, '국세청 종합소득세 기본세율 · 조세특례제한법 제104조의27 · 소득세법 제62조로 계산(2026.11.9)', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.33, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 한눈에 — 세 칸
fig = plt.figure(figsize=(9, 5.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.88, '고배당 ETF 분배금 세금, 내 경우는?', fontproperties=Bs(22), color=INK)
L = [('1년 배당·이자 2천만원 이하', 'ETF든 직접이든 15.4%로 같아요'),
     ('2천만원 넘고, 다른 소득 과세표준 4천만원 이하(배당 3천만원 예)', 'ETF가 오히려 덜 내기도 해요'),
     ('2천만원 넘고, 다른 소득 과세표준 5천만원 이상(배당 3천만원 예)', '직접 갖고 분리과세 신청한 쪽이 덜 내요')]
for i, (a, b) in enumerate(L):
    y = 0.68 - i * 0.22
    fig.patches.append(plt.Rectangle((0.05, y - 0.07), 0.9, 0.17, transform=fig.transFigure, color='#F3F4F6', zorder=0))
    fig.text(0.08, y + 0.035, a, fontproperties=Bs(15), color=SUB)
    fig.text(0.08, y - 0.035, b, fontproperties=Bs(18), color=ORG if i == 2 else INK)
fig.text(0.05, 0.03, 'ISA 안에서 받으면 200만원(서민형 400만원)까지 세금 없음 · 2026.11.9 기준', fontsize=11.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
