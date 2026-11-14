# mokpair1115 본문 그림 — 01 64~67㎡ 단지별 한 채 중간값, 02 7단지·11단지 1년 전 vs 최근 1년 (표지 00은 cafecover.py). 숫자는 calc_out·calc4_out 그대로
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, GR, SUBC, ORG = '#1D4ED8', '#93C5FD', '#111827', '#CBD5E1', '#6B7280', '#EA580C'
SRC = '국토교통부 아파트 매매 실거래(11/15 받음, 해제 제외) · 파이어맵 계산'
def eok(v): a = int(v); r = round((v - a) * 10000); return f'{a}억' + (f' {r//1000}천' if r and r % 1000 == 0 else (f' {r:,}' if r else '')) + '만원' if r else f'{a}억원'
rows = [('7단지', 25.40, 25), ('5단지', 25.00, 5), ('2단지', 23.60, 5), ('3단지', 23.50, 29), ('4단지', 23.50, 7), ('1단지', 23.00, 19), ('11단지', 20.00, 19)]
fig, ax = plt.subplots(figsize=(9, 7.0), dpi=100)
ys = list(range(len(rows)))[::-1]
for y, (n, v, c) in zip(ys, rows):
    col = ORG if n in ('7단지', '11단지') else LBLUE
    ax.barh(y, v, height=0.62, color=col)
    ax.text(v + 0.3, y, f'{eok(v)}  ({c}건)', va='center', fontproperties=Bs(15), color=INK)
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(17)); ax.set_xticks([]); ax.set_xlim(0, 36)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '목동신시가지 전용 64~67㎡ 한 채 중간값', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.885, '최근 1년(2025년 11월~2026년 11월 계약) · 이 크기 거래가 꾸준한 7개 단지', fontsize=13, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.85, bottom=0.07, left=0.13, right=0.98)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
grp = [('1년 전\n(24.11~25.10)', 22.00, 15.00), ('최근 1년\n(25.11~26.11)', 25.40, 20.00)]
for i, (lb, a, b) in enumerate(grp):
    ax.bar(i - 0.19, a, width=0.36, color=BLUE); ax.bar(i + 0.19, b, width=0.36, color=ORG)
    ax.text(i - 0.19, a + 0.5, eok(a), ha='center', fontproperties=Bs(15), color=INK)
    ax.text(i + 0.19, b + 0.5, eok(b), ha='center', fontproperties=Bs(15), color=INK)
    ax.text(i, max(a, b) + 3.4, f'차이 {eok(a-b)}', ha='center', fontproperties=Bs(19), color=ORG if i else SUBC)
ax.set_xticks([0, 1]); ax.set_xticklabels([g[0] for g in grp], fontproperties=Bs(16)); ax.set_yticks([]); ax.set_ylim(0, 33)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.bar(0, 0, color=BLUE, label='7단지'); ax.bar(0, 0, color=ORG, label='11단지')
ax.legend(loc='upper left', prop=Bs(14), frameon=False)
fig.text(0.04, 0.92, '7단지와 11단지, 같은 크기 차이가 줄었어요', fontproperties=Bs(23), color=INK)
fig.text(0.04, 0.865, '전용 64~67㎡ 한 채 중간값 · 평당 차이 46% → 28%', fontsize=14.5, color=SUBC)
fig.text(0.04, 0.03, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.8, bottom=0.2, left=0.06, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
