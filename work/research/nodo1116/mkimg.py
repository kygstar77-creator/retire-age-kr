# nodo1116 본문 그림 — 01 같은 집 기준 1년 새 오른 폭(구), 02 서울 아파트 거래 중 노도강 몫(월). 표지 00은 cafecover.py. 숫자는 calc_out·calc2_out 그대로
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, SUBC, ORG, GRY = '#1D4ED8', '#93C5FD', '#111827', '#6B7280', '#EA580C', '#CBD5E1'
SRC = '국토교통부 아파트 매매 실거래(11/15 받음, 해제 제외) · 파이어맵 계산'
rows = [('성동구', 27.4, LBLUE), ('송파구', 25.4, LBLUE), ('광진구', 25.0, LBLUE), ('노도강 뺀 22개 구', 15.5, BLUE),
        ('노원구 (20번째)', 8.2, ORG), ('강북구 (21번째)', 8.1, ORG), ('도봉구 (24번째)', 6.2, ORG), ('금천구 (25번째)', 4.5, GRY)]
fig, ax = plt.subplots(figsize=(9, 7.2), dpi=100)
ys = list(range(len(rows)))[::-1]
for y, (n, v, c) in zip(ys, rows):
    ax.barh(y, v, height=0.62, color=c)
    ax.text(v + 0.4, y, f'{v}%', va='center', fontproperties=Bs(16), color=INK)
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(15)); ax.set_xticks([]); ax.set_xlim(0, 33)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '같은 집 값, 1년 새 얼마나 올랐나', fontproperties=Bs(22), color=INK)
fig.text(0.04, 0.885, '같은 단지·같은 크기 묶음의 중간값 변화 · 최근 1년 vs 그 전 1년', fontsize=13, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.85, bottom=0.07, left=0.27, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
mon = ['24.11','24.12','25.1','25.2','25.3','25.4','25.5','25.6','25.7','25.8','25.9','25.10','25.11','25.12','26.1','26.2','26.3','26.4','26.5','26.6','26.7','26.8','26.9','26.10']
sh = [12.2,10.8,9.8,8.7,8.4,11.9,10.4,11.0,12.7,13.8,10.1,10.7,11.8,15.9,15.1,20.1,20.4,18.6,15.7,20.1,19.4,22.9,20.5,19.7]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
xs = range(len(mon))
ax.bar(xs, sh, width=0.7, color=[GRY if i < 12 else ORG for i in xs])
for i in (0, 11, 21, 23): ax.text(i, sh[i] + 0.5, f'{sh[i]}%', ha='center', fontproperties=Bs(14), color=INK)
ax.set_xticks([0, 6, 12, 18, 23]); ax.set_xticklabels(['2024.11', '2025.5', '2025.11', '2026.5', '2026.10'], fontsize=12.5)
ax.set_yticks([]); ax.set_ylim(0, 27)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.92, '서울 아파트 거래 중 노도강 몫', fontproperties=Bs(23), color=INK)
fig.text(0.04, 0.865, '1년 합으로 10.6% → 18.2% · 2026년 8월 22.9%(다섯 채 중 한 채 넘음)', fontsize=14, color=SUBC)
fig.text(0.04, 0.025, SRC + ' · 계약 월 기준', fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
