# k1pair1110 그림 2장 — 숫자는 calc_out.txt(금감원 금융상품한눈에 주담대 공시 2026.10, 한국은행 2021.08 고정형 평균)
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
# 01 한 달 납입액: 2021년 vs 고정형으로 다시 정할 때(은행 공시 낮은·가운데·높은)
rows = [('2021년 처음 (2.98%)', 126, LG, 0), ('낮은 쪽 4.92%', 155, BLU, 28), ('중간 5.45%', 163, ORG, 37), ('높은 쪽 6.03%', 172, BLU, 46)]  # 차는 calc_out 원 단위(284,663·367,760·461,162)에서 반올림
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
for i, (n, v, c, d) in enumerate(rows):
    ax.bar(i, v, color=c, width=0.6)
    ax.text(i, v + 3, f'{v}만원', ha='center', fontproperties=Bs(17), color=ORG if c == ORG else INK)
    if i: ax.text(i, v / 2, f'+{d}만원', ha='center', fontproperties=Bs(14), color='white')
ax.set_xticks(range(4)); ax.set_xticklabels([r[0] for r in rows], fontproperties=Bs(13))
ax.set_ylim(0, 200); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='x', length=0)
fig.text(0.05, 0.93, '5년 고정 끝나고 고정형으로 다시 정하면 한 달 얼마', fontproperties=Bs(20), color=INK)
fig.text(0.05, 0.885, '2021년 8월 3억원·30년 원리금균등 → 남은 2억 6,662만원을 25년으로 다시 계산(가정)', fontsize=12, color=SUB)
fig.text(0.05, 0.02, '금감원 금융상품한눈에 아파트 주담대 고정금리 15개 상품 공시(2026.10) · 한국은행 고정형 평균(2021.08)', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 한눈에 — 세 칸
fig = plt.figure(figsize=(9, 5.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.88, '고정 끝나기 전에 볼 것 세 가지', fontproperties=Bs(22), color=INK)
L = [('약정서', '고정이 끝나는 날과 그 뒤 기준금리 이름'),
     ('기준금리 발표일', '코픽스 10월분은 11월 16일에 나와요'),
     ('은행에 묻기', '내 대출에 붙을 금리로 한 달 납입액 다시 계산')]
for i, (a, b) in enumerate(L):
    y = 0.68 - i * 0.22
    fig.patches.append(plt.Rectangle((0.05, y - 0.07), 0.9, 0.17, transform=fig.transFigure, color='#F3F4F6', zorder=0))
    fig.text(0.08, y + 0.035, a, fontproperties=Bs(15), color=SUB)
    fig.text(0.08, y - 0.035, b, fontproperties=Bs(18), color=ORG if i == 2 else INK)
fig.text(0.05, 0.03, '공시 금리는 지난달 새로 빌린 사람들의 평균 · 2026.11.9 기준', fontsize=11.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
