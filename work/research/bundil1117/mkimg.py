# bundil1117 본문 그림 — 01 2023년 상반기→2026년 6~10월 같은 집 변화(구별), 02 2021년 하반기→2026년 6~10월. 표지 00은 cafecover.py. 숫자는 calc_out 그대로
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, SUBC, ORG, GRY = '#1D4ED8', '#93C5FD', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 화성시 동탄구(11/16 받음, 취소 거래 뺌) · 파이어맵 계산'
ms = ['25.1','2','3','4','5','6','7','8','9','10','11','12','26.1','2','3','4','5','6','7','8','9','10']
SRC = '국토교통부 아파트 매매 실거래 · 분당구·일산동구·일산서구(11/17 받음, 취소 거래 뺌) · 파이어맵 계산'
def bars(fname, title, sub, labs, vals, cnts, lo, hi):
    fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
    cols = [BLUE if v > 0 else ORG for v in vals]
    ax.bar(range(len(vals)), vals, color=cols, width=0.55)
    ax.axhline(0, color=INK, lw=1)
    for i, v in enumerate(vals):
        ax.text(i, v + (2.2 if v > 0 else -2.2), f'{v:+.0f}%', ha='center', va='bottom' if v > 0 else 'top', fontproperties=Bs(21), color=INK)
        ax.text(i, (1.5 if v < 0 else -1.5), f'{cnts[i]}곳', ha='center', va='bottom' if v < 0 else 'top', fontproperties=Bs(12.5), color=SUBC)
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labs, fontproperties=Bs(15))
    ax.tick_params(axis='x', length=0, pad=-2)
    for t in ax.get_xticklabels(): t.set_y(-0.0)
    ax.set_yticks([]); ax.set_ylim(lo, hi)
    for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
    fig.subplots_adjust(top=0.83, bottom=0.12, left=0.04, right=0.98)
    fig.savefig(fname, dpi=100); plt.close(fig)
bars('pkg/img/01.png', '같은 평형, 2023년 상반기보다 얼마나', '2023년 1~6월과 올해 6~10월에 모두 팔린 같은 단지·같은 넓이 집 · 가운데 값',
     ['분당구', '일산동구', '일산서구'], [63.2, -1.9, -4.9], [382, 172, 245], -22, 80)
bars('pkg/img/02.png', '같은 평형, 2021년 하반기보다 얼마나', '2021년 7~12월과 올해 6~10월에 모두 팔린 같은 단지·같은 넓이 집 · 가운데 값',
     ['분당구', '일산(동구+서구)'], [37.0, -23.7], [337, 472], -40, 52)
print('ok')
